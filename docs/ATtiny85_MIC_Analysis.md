# ATtiny85 MIC Debug Analysis

## The Problem
The MIC module's digital output (DO) is Active HIGH, continuity to ATtiny85 PB4 is confirmed, but the ESP32 never sees MIC triggers from the ATtiny85.

## ATtiny85 Input Voltage Thresholds

The ATtiny85 running at **5V VCC** has these input logic thresholds (from Atmel datasheet):

| Parameter | Symbol | Value |
|-----------|--------|-------|
| Input LOW (max) | V_IL | **0.3 × VCC = 1.5V** |
| Input HIGH (min) | V_IH | **0.6 × VCC = 3.0V** |

> [!WARNING]
> **If the MIC module outputs 2.5V as "HIGH" (common with 3.3V-logic LM393 modules), the ATtiny85 sees it as NEITHER HIGH nor LOW — it's in the "undefined zone" between 1.5V and 3.0V.** This would cause `digitalRead(MIC_IN_PIN)` to return random/stuck values, and the pin-change interrupt would never fire reliably.

### Common MIC Module Voltage Scenarios

| MIC Module VCC | DO "HIGH" Output | ATtiny85 VIH (5V) | Detection |
|----------------|-------------------|-------------------|-----------|
| **5V** | ~4.5V | 3.0V | ✅ Works |
| **3.3V** | ~2.8V | 3.0V | ❌ **FAILS** — below threshold |
| **3.3V with pull-up** | ~4.7V | 3.0V | ✅ Works |

---

## Debug Firmware

Flash [fall_attiny_mic_debug.ino](file:///C:/Users/devja/Documents/Arduino/fall_attiny_mic_debug/fall_attiny_mic_debug.ino) to the ATtiny85. It does 3 things:

### 1. Startup Confirmation
- **5 rapid blinks on PB0** (MIC_OUT) at boot → confirms firmware is loaded

### 2. Live MIC Mirror on PB3
- PB3 (onboard LED on Digispark Model B) continuously mirrors `digitalRead(MIC_IN_PIN)`
- **If PB3 stays OFF during loud sounds** → MIC HIGH is below ATtiny85's VIH threshold (voltage problem)
- **If PB3 toggles with sound** → ATtiny85 IS detecting the MIC, bug is elsewhere

### 3. MIC Detection Blink Pattern
- On MIC state change: normal 50ms wake pulse on PB0, then **3 additional rapid blinks** (100ms each)
- Easy to distinguish from PIR (which is 1 long pulse on PB2)

### Pin Assignment Note

> [!NOTE]
> PB3 is the onboard LED on **Digispark Model B** boards. If your board has the LED on PB1, you'll see the PIR_IN_PIN conflicts with it. In that case, just observe MIC_OUT (PB0) — you can temporarily connect a standalone LED+resistor there, or just watch the ESP32 serial output for `[SYS]: MIC Triggered!`.

---

## Likely Fix: Voltage Level Mismatch

If the debug firmware confirms the MIC HIGH isn't crossing VIH:

### Option A: Power MIC module from 5V (Easiest)
If the MIC module (LM393-based) supports 5V input, power it from 5V instead of 3.3V. Its DO output will then swing to ~4.5V, well above the ATtiny85's 3.0V VIH.

### Option B: External Pull-Up Resistor (If MIC must stay 3.3V)
Add a **10kΩ pull-up resistor** from MIC_DO to 5V. The LM393's open-collector output will pull LOW on silence, and the pull-up pulls to 5V on sound.

```
5V ──┬── 10kΩ ──┬── ATtiny85 PB4
     │          │
     └── MIC DO ┘
```

> [!IMPORTANT]
> **The LM393 comparator has an open-collector output** — it can only pull LOW, not drive HIGH. Without a pull-up to the ATtiny85's VCC (5V), the "HIGH" level is determined by whatever weak pull-up or leakage current exists, which may not reach 3.0V.

### Option C: Change ATtiny85 VCC to 3.3V
Run the ATtiny85 at 3.3V. VIH becomes 0.6 × 3.3V = 1.98V, so a 2.8V MIC HIGH easily clears the threshold. BUT this changes all output levels too — the ESP32 input pins (3.3V logic) would be fine, but verify PIR module compatibility.

### Option D: Software Analog Threshold (Advanced)
Use `analogRead()` on PB4 instead of `digitalRead()` and set a custom threshold:

```cpp
int micRaw = analogRead(MIC_IN_PIN);  // 0-1023
bool currentMicState = (micRaw > 400); // ~2.0V threshold
```

This bypasses the ATtiny85's hardware VIH threshold entirely. Requires changing PB4 to ADC2 and using the ATtiny85's built-in ADC.

---

## After Debugging

Once the MIC issue is resolved, **reflash the production firmware** [fall_attiny_v1.ino](file:///C:/Users/devja/Documents/Arduino/fall_attiny_v1/fall_attiny_v1.ino).
