# 📱 Fall Sensor Mobile App (Android Companion)

An Android companion application built for caregivers and clinicians to monitor fall events, room occupancy, and device health over Bluetooth Low Energy (BLE).

---

## 🛠️ Architecture & Tech Stack

* **Language:** 100% Kotlin
* **UI Framework:** Jetpack Compose + Material 3 (Dark Theme)
* **Architecture:** MVVM (Model-View-ViewModel) with Kotlin Coroutines & `StateFlow`
* **Connectivity:** Android Bluetooth Low Energy (GATT Client) with automatic background reconnection and state recovery.

---

## 🏷️ Product Flavors

The Gradle build configuration supports two hardware target flavors:

| Flavor | Target Sensor | BLE Scan Filter | Description |
|---|---|---|---|
| **`c1001`** | DFRobot C1001 (60 GHz) | `FallSensor_C1001*` | Ceiling-mounted sensor UI with target distance-to-ceiling display and human presence flags. |
| **`ld2410`** | Hi-Link LD2410 (24 GHz) | `FallSensor_LD2410*` | Wall-mounted sensor UI with moving/stationary gate distance metrics. |

---

## ⚡ Core Features

1. **Real-Time Telemetry Dashboard:**
   * Live battery voltage and dynamic discharge curve lifetime forecasting.
   * Uptime counter (`Xh Ym Zs`).
   * Room occupancy status (`OCCUPIED` vs `VACANT`) with 4 animated sensor indicators.
2. **Instant Fall Alert Display:**
   * High-visibility alert banners triggered immediately upon receiving `ALERT: FALL DETECTED` packets.
   * Visual reset and disarm controls via the BLE `RESET` command.
3. **Caregiver Configuration & Diagnostics:**
   * **Room Height Configuration:** Send `SET:HEIGHT:<cm>` to calibrate floor threshold in the sensor's non-volatile memory.
   * **Telemetry Logging Toggle:** `LOG_ON` and `LOG_OFF` commands to inspect raw 100ms radar gate packets without draining battery during normal use.
   * **Over-the-Air Update Trigger:** `OTA_ON` command to put the sensor into firmware update mode.

---

## 📡 BLE GATT Specifications

* **Service UUID:** `4fafc201-1fb5-459e-8fcc-c5c9c331914b`
* **Telemetry Characteristic UUID:** `beb5483e-36e1-4688-b7f5-ea07361b26a8` (Read, Write, Notify)

---

## 🚀 Building & Running

### Requirements
* Android Studio Iguana / Jellyfish (or newer)
* Android SDK 34 (Android 14)
* Minimum SDK: Android 26 (Android 8.0 Oreo)

### Build Commands
```bash
# Build C1001 Ceiling Flavor Debug APK
./gradlew assembleC1001Debug

# Build LD2410 Wall Flavor Debug APK
./gradlew assembleLd2410Debug
```
Output APKs will be generated in `app/build/outputs/apk/<flavor>/debug/`.
