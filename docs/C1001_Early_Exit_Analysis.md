# C1001 Early Exit Bug Report

## Symptom
LD2410 correctly early-exits at 2501ms. C1001 runs the full 30-second snapshot despite `UART Pres: 1`.

## Root Cause Analysis

### 🐛 Bug #1: `hu.getFallData()` Called TWICE Per Loop — UART Corruption

```cpp
// Line 509 — C1001
bool uartFall = (hu.getFallData(hu.eFallState) == 1 || hu.getFallData(hu.eFallState) == 2);
//               ^^^^^^^^^ CALL 1 (UART TX/RX)        ^^^^^^^^^ CALL 2 (UART TX/RX)
```

Each `hu.getFallData()` sends a UART command and waits for a response. Calling it **twice in the same expression** means:
1. First call: sends command, reads response → maybe returns 0
2. The `||` short-circuits IF the first call returned 1, but if it returned 0...
3. Second call: sends another command **immediately**, potentially reading a response frame that belongs to the FIRST call's response tail

**This corrupts the DFRobot UART state machine**, causing subsequent `hu.dmHumanData()` calls in later iterations to return garbage/0 instead of the real value.

> [!IMPORTANT]
> The LD2410 library does NOT have this problem. `radar.read()` parses the ENTIRE serial buffer once, then all subsequent `.presenceDetected()`, `.movingTargetDistance()` etc. calls just read from the already-parsed data — no additional UART transactions.

---

### 🐛 Bug #2: 3–4 Blocking UART Calls Per Loop Iteration

Each C1001 loop iteration does:

| Call | UART Transaction | Est. Time |
|------|-----------------|-----------|
| `hu.dmHumanData(hu.eExistence)` | Send cmd + wait response | ~200–500ms |
| `hu.getFallData(hu.eFallState)` — call 1 | Send cmd + wait response | ~200–500ms |
| `hu.getFallData(hu.eFallState)` — call 2 | Send cmd + wait response | ~200–500ms |
| `hu.dmHumanData(hu.eMotionHorizontalDistance)` | Send cmd + wait response (if presence) | ~200–500ms |

**Total per iteration: ~800ms–2000ms** (vs. the LD2410 which takes <1ms for a `digitalRead`)

Your log confirms this — the 10-second heartbeat logs appear at exactly 11-second intervals (13:33:18 → 13:33:29 → 13:33:40), which is the heartbeat interval + UART overhead per iteration.

The early exit check runs **after** all these UART calls. If any UART call blocks or returns corrupted data (due to Bug #1), `presenceDetected` could be `false` on iterations where the early exit check actually fires.

---

### 🐛 Bug #3: `hardwarePresence` Hardcoded to `false` — No GPIO Fast-Path

```cpp
// C1001 — Line 512
bool hardwarePresence = false;  // ← DISABLED FOR DIAGNOSTIC
bool presenceDetected = hardwarePresence || uartPresence;
```

vs. LD2410:
```cpp
// LD2410 — Line 518
bool presenceDetected = digitalRead(PRESENCE_PIN);  // ← FAST GPIO
// Line 610
bool isOccupiedNow = (presenceDetected || radar.presenceDetected());
```

The LD2410 early exit is driven by `digitalRead(PRESENCE_PIN)` which is **instantaneous and always reliable**. Even when the LD2410 UART returns `UART Pres: 0` (as in your log!), the GPIO pin returns 1, so the early exit fires.

The C1001 **has no GPIO fast-path** — it relies entirely on the slow, potentially-corrupted UART path.

---

## Evidence From Your Logs

### LD2410 (Early Exit WORKS ✅)
```
[RADAR] Pin25_RAW: 1 | UART Pres: 0 | Dist: 0cm (M:0 S:0)
                   ^               ^
                   GPIO=1 (FAST)   UART=0 (irrelevant, GPIO already true)
→ Fast Occupancy Confirmed (Early Exit at 2501ms)
```

### C1001 (Early Exit FAILS ❌)
```
[RADAR] Pin25_RAW: 0 | Pin26_RAW: 0 | UART Pres: 1 | UART Fall: 0 | Dist: 300cm
                   ^                                  ^
                   GPIO=0 (but hardcoded false anyway) UART=1 (logged snapshot only)
→ Startup Check Complete (snapshotTimeout at 30s)
```

The LD2410 early-exits because GPIO Pin25 is HIGH immediately. The C1001 shows `UART Pres: 1` in the heartbeat log, but between logged iterations, the UART value likely fluctuates due to the double-call corruption in Bug #1.

---

## Proposed Fixes

### Fix 1: Cache the fall UART result (eliminates double-call corruption)

```diff
-      bool uartFall = (hu.getFallData(hu.eFallState) == 1 || hu.getFallData(hu.eFallState) == 2);
+      int fallState = hu.getFallData(hu.eFallState);
+      bool uartFall = (fallState == 1 || fallState == 2);
```

### Fix 2: Enable the GPIO fast-path for presence detection

```diff
-      bool hardwarePresence = false;
+      bool hardwarePresence = (rawPin25 == HIGH);
```

This gives the C1001 the same GPIO fast-path as the LD2410. Even if UART is slow/corrupt, the GPIO pin can drive the early exit.

> [!NOTE]  
> Your Pin25_RAW is currently showing `0` — the C1001's OUT1 pin may need configuration via the DFRobot library or a wiring check. If OUT1 is genuinely not outputting presence, this fix alone won't help. But it's the correct architectural fix.

### Fix 3: Add UART read timeout protection

```diff
+      // Read UART with timeout protection
+      unsigned long uartStart = millis();
       bool uartPresence = (hu.dmHumanData(hu.eExistence) == 1);
+      if (millis() - uartStart > 1000) {
+          // UART is hanging. Use last known good value.
+          uartPresence = lastLoggedUARTPres;
+      }
```

---

## Summary

| Bug | Severity | Impact |
|-----|----------|--------|
| Double UART call for fall data | **HIGH** | Corrupts UART buffer, causes intermittent `uartPresence = false` |
| 3-4 blocking UART calls per loop | **MEDIUM** | Slows loop to ~1-2 Hz, reduces chances of catching early exit window |
| `hardwarePresence` disabled | **HIGH** | No GPIO fast-path fallback, 100% reliance on fragile UART |
