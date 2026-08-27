// VERSION: v4.22 - Ceiling Height Setting (9ft Default) + Floor-Level Static Fall Detection (2026-08-27)

#include <WiFi.h>
#include <ArduinoOTA.h>
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>
#include <DFRobot_HumanDetection.h>
#include <driver/rtc_io.h>

// --- USER CONFIGURABLE CEILING & ROOM HEIGHT SETTINGS ---
// Default: 9 feet = 274 cm (persists across deep sleep cycles in RTC memory)
RTC_DATA_ATTR int roomHeightCm = 274;         
RTC_DATA_ATTR int floorToleranceCm = 45;      // Target detected between (roomHeight - 45) and (roomHeight + 35) is at floor level
RTC_DATA_ATTR int floorLyingConsecutiveChecks = 0; // Number of consecutive periodic checks target remains on floor
const int FLOOR_LYING_ALERT_THRESHOLD = 2;   // 2 consecutive checks (~60-120s) triggers static fall alarm

// --- HARDWARE PINS ---
#define PIR_WAKE_PIN     13  
#define MIC_WAKE_PIN     4   
#define PRESENCE_PIN     25  // C1001 OUT1
#define FALL_PIN         26  // C1001 OUT2
#define SYNC_BUTTON_PIN  33  
#define BATTERY_PIN      34  
#define RADAR_MOSFET_PIN 27  
#define FALL_LED_PIN     19  
#define RX_PIN           16  
#define TX_PIN           17  

// --- BLE UUIDS ---
#define SERVICE_UUID           "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define CHARACTERISTIC_UUID    "beb5483e-36e1-4688-b7f5-ea07361b26a8"

BLEServer* pServer = NULL;
BLECharacteristic* pCharacteristic = NULL;
bool deviceConnected = false;
bool isBleAdvertising = false;
unsigned long bleTurnedOnTime = 0;
bool debugMode = false;

// --- STATE & TIMERS ---
RTC_DATA_ATTR int bootCount = 0;
RTC_DATA_ATTR bool wasOccupied = false; // Remembers occupancy across deep sleep
unsigned long lastPirLogTime = 0;
unsigned long lastMicLogTime = 0;
RTC_DATA_ATTR int occupiedCount = 0;  // consecutive occupied snapshots for sleep backoff

enum TriggerSource { BOOT, PIR_WALK_IN, MIC_THUD, MANUAL_SYNC, PERIODIC_TIMER };
TriggerSource currentTrigger = BOOT;

uint64_t PERIODIC_SLEEP_SEC = 60; // Configurable periodic sleep

bool isRadarPowered = false;
unsigned long radarTurnedOnTime = 0;
unsigned long lastLedFlash = 0;
unsigned long lastDebugLog = 0;

// Smart logging: track last values to only log on change or 10s heartbeat
bool lastLoggedHWPres = false;
bool lastLoggedUARTPres = false;
bool lastLoggedHWFall = false;
bool lastLoggedUARTFall = false;
uint16_t lastLoggedDist = 0;
unsigned long lastHeartbeatLog = 0;
const unsigned long HEARTBEAT_LOG_INTERVAL = 10000;  // 10 seconds

bool fallConfirmed = false;
unsigned long sustainedMoveStartTime = 0;
bool batteryReported = false;
bool batteryCritical = false;

volatile bool syncButtonPressed = false;
volatile bool pirTriggered = false;
volatile bool micTriggered = false;
bool requestRadarPowerOn = false;

// Sensor Fusion Tracking
bool pirSeenInSnapshot = false;
bool micSeenInSnapshot = false;

// Fake Sleep (When BLE is connected)
bool isFakeSleeping = false;
bool infiniteFakeSleep = false;
unsigned long fakeSleepStartTime = 0;

const unsigned long DEBOUNCE_COOLDOWN = 3000;
unsigned long lastSleepTime = 0;  // PIR cooldown: ignore PIR for 5s after sleeping
const unsigned long PIR_COOLDOWN_MS = 5000;

#define WIFI_SSID "Jio-ruby105"
#define WIFI_PASS "Pumba@6969"
bool otaActive = false;
unsigned long otaStartTime = 0;
bool requestOtaStart = false;
bool otaConnecting = false;
unsigned long otaConnectStartTime = 0;
bool otaDisconnectBlePending = false;
unsigned long otaDisconnectBleTime = 0;

HardwareSerial RadarSerial(1);
DFRobot_HumanDetection hu(&RadarSerial);

void startBLE();
void stopBLE();
void powerOnRadar();
void goToSleep(bool infinite);

class MyServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
      deviceConnected = true;
      isBleAdvertising = false;
      batteryReported = false; 
      bleTurnedOnTime = millis();
    }
    void onDisconnect(BLEServer* pServer) {
      deviceConnected = false;
      isFakeSleeping = false;
      // Auto LOG_OFF: stop wasting resources logging to nobody
      if (debugMode) {
          debugMode = false;
      }
      // Auto OTA_OFF: don't leave WiFi running with no controller
      if (otaActive) {
          otaActive = false;
          WiFi.disconnect(true);
          WiFi.mode(WIFI_OFF);
      }
      // If we disconnect while fake sleeping, immediately real sleep
      if (!isRadarPowered) goToSleep(infiniteFakeSleep);
    }
};

void IRAM_ATTR syncButtonISR() { syncButtonPressed = true; }
void IRAM_ATTR pirISR() { pirTriggered = true; }
void IRAM_ATTR micISR() { micTriggered = true; }

class MyCallbacks: public BLECharacteristicCallbacks {
    void onWrite(BLECharacteristic *pChar) {
      String rxValue = pChar->getValue(); 
      if (rxValue.length() > 0) {
        if (rxValue.indexOf("LOG_ON") != -1) {
          if (debugMode) {
              pChar->setValue("Debug Mode: Already ON. Ignoring.\n");
              pChar->notify();
          } else {
              debugMode = true;
              pChar->setValue("Debug Mode: ENABLED\n");
              pChar->notify();
              requestRadarPowerOn = true;
          }
        }
        else if (rxValue.indexOf("LOG_OFF") != -1) {
          debugMode = false;
          pChar->setValue("Debug Mode: DISABLED\n");
          pChar->notify();
        }
        else if (rxValue.startsWith("SET:HEIGHT:")) {
          int newH = rxValue.substring(11).toInt();
          if (newH >= 150 && newH <= 500) {
              roomHeightCm = newH;
              String reply = "[CFG] Room Height set to " + String(roomHeightCm) + " cm (" + String(roomHeightCm / 30.48, 1) + " ft)\n";
              pChar->setValue(reply.c_str());
              pChar->notify();
          }
        }
        else if (rxValue.indexOf("OTA_ON") != -1) {
          if (otaActive || otaConnecting || requestOtaStart) {
              pChar->setValue("[OTA] Already starting or active. Ignoring.\n");
              pChar->notify();
          } else {
              pChar->setValue("[OTA] Initiating... Powering down Radar & connecting to WiFi.\n");
              pChar->notify();
              requestOtaStart = true;
          }
        }
      }
    }
};

void startBLE() {
  BLEDevice::startAdvertising();
  isBleAdvertising = true;
  bleTurnedOnTime = millis();
}

void stopBLE() {
  BLEDevice::stopAdvertising();
  isBleAdvertising = false;
}

void sendBLENotification(const char* message) {
  if (deviceConnected) {
    pCharacteristic->setValue(message);
    pCharacteristic->notify();
  }
}

void goToSleep(bool infinite) {
  // If OTA is active or connecting, we can't sleep but we MUST still turn off the radar
  // to prevent the 30-second snapshot from spam-firing every loop iteration
  if (otaActive || otaConnecting) {
      if (isRadarPowered) {
          digitalWrite(RADAR_MOSFET_PIN, LOW);
          digitalWrite(FALL_LED_PIN, LOW);
          isRadarPowered = false;
      }
      return;
  }
  if (fallConfirmed) {
      radarTurnedOnTime = millis(); // Reset timer to prevent 1000Hz re-trigger loop while alarm active
      return;
  }

  digitalWrite(RADAR_MOSFET_PIN, LOW);
  digitalWrite(FALL_LED_PIN, LOW);
  isRadarPowered = false;

  if (deviceConnected) {
      // Fake Sleep Mode
      isFakeSleeping = true;
      infiniteFakeSleep = infinite;
      fakeSleepStartTime = millis();
      
      if (infinite) {
          // If sensor fusion warning will trigger, don't say room empty yet!
          if (!(pirSeenInSnapshot && micSeenInSnapshot)) {
              sendBLENotification("[SYS]: Room Empty. Going to Deep Sleep indefinitely...\n");
          }
      }
      else sendBLENotification("[SYS]: All OK. Going on standby for 60s...\n");
      // Auto log reset logic handled by timestamp tracking
      return; 
  }

  // Session logs reset handled by time, no need to reset vars
  
  if (isBleAdvertising) stopBLE();
  if (otaActive) { WiFi.disconnect(true); otaActive = false; }
  
  if (infinite) {
      // Infinite sleep: wake on PIR, MIC, or SYNC button
      uint64_t bitmask = (1ULL << PIR_WAKE_PIN) | (1ULL << MIC_WAKE_PIN) | (1ULL << SYNC_BUTTON_PIN);
      esp_sleep_enable_ext1_wakeup(bitmask, ESP_EXT1_WAKEUP_ANY_HIGH);
  } else {
      // Periodic 60s sleep: Allow Acoustic Impact THUD (MIC) and SYNC button to interrupt immediately!
      // (PIR walking motion is ignored to prevent battery drain in occupied room)
      uint64_t bitmask = (1ULL << SYNC_BUTTON_PIN) | (1ULL << MIC_WAKE_PIN);
      esp_sleep_enable_ext1_wakeup(bitmask, ESP_EXT1_WAKEUP_ANY_HIGH);
      esp_sleep_enable_timer_wakeup(PERIODIC_SLEEP_SEC * 1000000ULL);
  }
  
  pirTriggered = false;
  micTriggered = false;
  lastSleepTime = millis();
  
  esp_deep_sleep_start();
}

void powerOnRadar() {
  digitalWrite(RADAR_MOSFET_PIN, HIGH);
  digitalWrite(FALL_LED_PIN, HIGH);
  delay(1500);  // Allow C1001 1.5s to boot hardware & UART

  isRadarPowered = true;
  radarTurnedOnTime = millis();
  isFakeSleeping = false;
  
  // Reset fusion flags for this new session
  pirSeenInSnapshot = (currentTrigger == PIR_WALK_IN);
  micSeenInSnapshot = (currentTrigger == MIC_THUD);

  if (debugMode) {
      String onMsg = "[RADAR]: Boot. Trigger: ";
      switch(currentTrigger) {
        case PIR_WALK_IN: onMsg += "PIR\n"; break;
        case MIC_THUD:    onMsg += "MIC\n"; break;
        case PERIODIC_TIMER: onMsg += "Periodic 60s Timer\n"; break;
        default:          onMsg += "System\n"; break;
      }
      sendBLENotification(onMsg.c_str());
  }
}

float readBatteryVoltage() {
  int rawValue = analogRead(BATTERY_PIN);
  return (rawValue / 4095.0) * 3.3 * 2.0; 
}

void setup() {
  pinMode(RADAR_MOSFET_PIN, OUTPUT);
  pinMode(FALL_LED_PIN, OUTPUT);
  pinMode(PRESENCE_PIN, INPUT_PULLUP);
  pinMode(FALL_PIN, INPUT_PULLUP);
  pinMode(SYNC_BUTTON_PIN, INPUT_PULLDOWN);
  pinMode(PIR_WAKE_PIN, INPUT_PULLDOWN);
  pinMode(MIC_WAKE_PIN, INPUT_PULLDOWN);
  
  rtc_gpio_pulldown_en((gpio_num_t)PIR_WAKE_PIN);
  rtc_gpio_pulldown_en((gpio_num_t)MIC_WAKE_PIN);
  rtc_gpio_pullup_dis((gpio_num_t)MIC_WAKE_PIN);
  rtc_gpio_pulldown_en((gpio_num_t)SYNC_BUTTON_PIN);

  attachInterrupt(digitalPinToInterrupt(SYNC_BUTTON_PIN), syncButtonISR, RISING);
  attachInterrupt(digitalPinToInterrupt(PIR_WAKE_PIN), pirISR, RISING);
  attachInterrupt(digitalPinToInterrupt(MIC_WAKE_PIN), micISR, RISING);

  digitalWrite(RADAR_MOSFET_PIN, LOW);
  digitalWrite(FALL_LED_PIN, LOW);

  BLEDevice::init("Fall_Sensor_C1001_v4.22");
  pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());
  BLEService *pService = pServer->createService(SERVICE_UUID);
  pCharacteristic = pService->createCharacteristic(
                      CHARACTERISTIC_UUID,
                      BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_WRITE | BLECharacteristic::PROPERTY_NOTIFY
                    );
  pCharacteristic->setCallbacks(new MyCallbacks());
  pCharacteristic->addDescriptor(new BLE2902());
  pService->start();

  RadarSerial.begin(115200, SERIAL_8N1, RX_PIN, TX_PIN); 
  
  if (readBatteryVoltage() < 3.3) {
      batteryCritical = true;
  }
  
  esp_sleep_wakeup_cause_t wakeup_reason = esp_sleep_get_wakeup_cause();
  if (wakeup_reason == ESP_SLEEP_WAKEUP_EXT1) {
    uint64_t wakeup_pin_mask = esp_sleep_get_ext1_wakeup_status();
    if (wakeup_pin_mask & (1ULL << PIR_WAKE_PIN)) {
      currentTrigger = PIR_WALK_IN;
      lastPirLogTime = 0; // Force immediate log
    } else if (wakeup_pin_mask & (1ULL << MIC_WAKE_PIN)) {
      currentTrigger = MIC_THUD;
      lastMicLogTime = 0; // Force immediate log
    } else if (wakeup_pin_mask & (1ULL << SYNC_BUTTON_PIN)) {
      currentTrigger = MANUAL_SYNC;
      startBLE(); 
      return; // Skip radar for manual sync
    }
    powerOnRadar();
  } else if (wakeup_reason == ESP_SLEEP_WAKEUP_TIMER) {
      currentTrigger = PERIODIC_TIMER;
      powerOnRadar();
  } else {
      currentTrigger = BOOT;
      powerOnRadar();  
  }
}

void loop() {
  // --- Asynchronous Non-blocking OTA Handler & Absolute Freeze Guard ---
  if (otaActive || otaConnecting || requestOtaStart || otaDisconnectBlePending) {
      if (isRadarPowered) {
          digitalWrite(RADAR_MOSFET_PIN, LOW);
          digitalWrite(FALL_LED_PIN, LOW);
          isRadarPowered = false;
      }
      if (requestOtaStart) {
          requestOtaStart = false;
          isFakeSleeping = false;
          WiFi.mode(WIFI_STA);
          WiFi.begin(WIFI_SSID, WIFI_PASS);
          otaConnecting = true;
          otaConnectStartTime = millis();
      }
      if (otaConnecting) {
          if (WiFi.status() == WL_CONNECTED) {
              otaConnecting = false;
              ArduinoOTA.begin();
              otaActive = true;
              otaStartTime = millis();
              String ipMsg = "[OTA] Ready at: " + WiFi.localIP().toString() + " | Disconnecting BLE to save power...\n";
              sendBLENotification(ipMsg.c_str());
              otaDisconnectBlePending = true;
              otaDisconnectBleTime = millis();
          } else if (millis() - otaConnectStartTime > 15000) {
              otaConnecting = false;
              WiFi.disconnect(true);
              WiFi.mode(WIFI_OFF);
              sendBLENotification("[OTA] WiFi connection failed. Restoring normal mode.\n");
              powerOnRadar();
          }
          return;
      }
      if (otaDisconnectBlePending) {
          if (millis() - otaDisconnectBleTime > 1000) {
              otaDisconnectBlePending = false;
              BLEDevice::deinit(false);
              deviceConnected = false;
              isBleAdvertising = false;
          }
      }
      if (otaActive) {
          ArduinoOTA.handle();
          if (millis() - otaStartTime > 300000) {
              WiFi.disconnect(true);
              ESP.restart();
          }
      }
      return; // Absolute block — no PIR/MIC interrupts or radar logic run while OTA active!
  }

  if (isFakeSleeping) {
      // Flush ghost interrupts while asleep unless they actually break the sleep
      if (!infiniteFakeSleep && (millis() - fakeSleepStartTime > PERIODIC_SLEEP_SEC * 1000)) {
          pirTriggered = false;
          micTriggered = false;
          currentTrigger = PERIODIC_TIMER;
          powerOnRadar();
          return;
      }
      // During periodic (non-infinite) fake sleep, we just LOG the PIR/MIC triggers 
      // so the user can see them, but we DO NOT wake the radar up.
      // Only the 60-second timer will actually wake the radar.
      if (!infiniteFakeSleep) {
          if (pirTriggered) {
              pirTriggered = false;
              if (deviceConnected && (millis() - lastPirLogTime > DEBOUNCE_COOLDOWN)) {
                  sendBLENotification("[SYS]: PIR Triggered! (Ignored during 60s sleep)\n");
                  lastPirLogTime = millis();
              }
          }
          if (micTriggered) {
              micTriggered = false;
              if (deviceConnected && (millis() - lastMicLogTime > DEBOUNCE_COOLDOWN)) {
                  sendBLENotification("[SYS]: MIC Triggered! (Ignored during 60s sleep)\n");
                  lastMicLogTime = millis();
              }
          }
      } else {
          // Infinite fake sleep: PIR/MIC CAN break it (room was empty, new activity)
          if (pirTriggered) {
              pirTriggered = false;
              micTriggered = false;
              currentTrigger = PIR_WALK_IN;
              powerOnRadar();
              return;
          }
          if (micTriggered) {
              micTriggered = false;
              pirTriggered = false;
              currentTrigger = MIC_THUD;
              powerOnRadar();
              return;
          }
      }
      return; // Skip rest of loop while in standby
  }

  // Live Interrupt Handling (with PIR cooldown to prevent wake/sleep loops)
  if (pirTriggered) {
      pirTriggered = false;
      // Ignore PIR if we just woke up less than 5s ago (residual heat)
      if (millis() - lastSleepTime < PIR_COOLDOWN_MS && lastSleepTime > 0) {
          // Silently discard — PIR is still seeing residual heat from before sleep
      } else {
          pirSeenInSnapshot = true;
          if (deviceConnected && (millis() - lastPirLogTime > DEBOUNCE_COOLDOWN)) {
              sendBLENotification("[SYS]: PIR Triggered!\n");
              lastPirLogTime = millis();
          }
          if (!isRadarPowered) { 
              currentTrigger = PIR_WALK_IN; 
              powerOnRadar(); 
          }
      }
  }

  if (micTriggered) {
      micTriggered = false; 
      micSeenInSnapshot = true;
      if (deviceConnected && (millis() - lastMicLogTime > DEBOUNCE_COOLDOWN)) {
          sendBLENotification("[SYS]: MIC Triggered!\n");
          lastMicLogTime = millis();
      }
      if (!isRadarPowered) { 
          currentTrigger = MIC_THUD; 
          powerOnRadar(); 
      }
  }

  if (requestRadarPowerOn && !isRadarPowered) {
      requestRadarPowerOn = false;
      currentTrigger = MANUAL_SYNC;
      powerOnRadar();
  }

  if (syncButtonPressed) {
      syncButtonPressed = false;
      if (fallConfirmed) {
          fallConfirmed = false;
          sustainedMoveStartTime = 0;
          digitalWrite(FALL_LED_PIN, HIGH);
          sendBLENotification("[FALL] Cleared: Manual Sync Button pressed.\n");
      }
      if (!isBleAdvertising && !deviceConnected) {
          startBLE();
      }
  }

  if (!isRadarPowered && isBleAdvertising && !deviceConnected) {
      if (millis() - bleTurnedOnTime > 60000) { goToSleep(true); }
  }

  if (deviceConnected && !batteryReported && (millis() - bleTurnedOnTime > 1500)) {
      float battV = readBatteryVoltage();
      String battMsg = "[SYS] Battery: " + String(battV, 2) + "V\n";
      if (batteryCritical) battMsg += "[WARN]: BATTERY CRITICAL (< 3.3V)!\n";
      sendBLENotification(battMsg.c_str());
      batteryReported = true;
  }

  // --- C1001 Radar Logic (Pins + UART Fallback) ---
  if (isRadarPowered) {
      
      int rawPin25 = digitalRead(PRESENCE_PIN);
      int rawPin26 = digitalRead(FALL_PIN);
      
      bool uartPresence = (hu.dmHumanData(hu.eExistence) == 1);
      int fallState = hu.getFallData(hu.eFallState);  // Cache result — calling twice corrupts UART buffer!
      bool uartFall = (fallState == 1 || fallState == 2);
      
      // Hardware Pin presence: GPIO fast-path for early exit (same pattern as LD2410)
      bool hardwarePresence = (rawPin25 == HIGH);
      bool hardwareFall = (rawPin26 == HIGH);
      
      bool presenceDetected = hardwarePresence || uartPresence;
      bool fallDetected = hardwareFall || uartFall;
      
      uint16_t dist = 0;
      if (uartPresence) { 
          dist = hu.dmHumanData(hu.eMotionHorizontalDistance); 
          if (dist == 0) {
              dist = hu.smHumanData(hu.eHumanDistance); // direct line-of-sight distance from ceiling
          }
      }

      // Check if target is at floor level (e.g. 9ft room: 274cm - 45cm = 229cm to 274cm + 35cm = 309cm)
      bool isAtFloorLevel = false;
      if (presenceDetected && dist > 0) {
          if (dist >= (roomHeightCm - floorToleranceCm) && dist <= (roomHeightCm + 35)) {
              isAtFloorLevel = true;
          }
      }

      if (debugMode) {
          // Smart logging: only log if values changed OR 10s heartbeat elapsed
          bool valuesChanged = (rawPin25 != lastLoggedHWPres) || (uartPresence != lastLoggedUARTPres) || (rawPin26 != lastLoggedHWFall) || (uartFall != lastLoggedUARTFall) || (dist != lastLoggedDist);
          bool heartbeatDue = (millis() - lastHeartbeatLog > HEARTBEAT_LOG_INTERVAL);
          if (valuesChanged || heartbeatDue) {
              String logMsg = "[RADAR] Pin25_RAW: " + String(rawPin25) + " | Pin26_RAW: " + String(rawPin26) + " | UART Pres: " + String(uartPresence) + " | UART Fall: " + String(uartFall) + " | Dist: " + String(dist) + "cm";
              if (isAtFloorLevel) logMsg += " [FLOOR LEVEL]";
              logMsg += "\n";
              sendBLENotification(logMsg.c_str());
              lastLoggedHWPres = rawPin25;
              lastLoggedUARTPres = uartPresence;
              lastLoggedHWFall = rawPin26;
              lastLoggedUARTFall = uartFall;
              lastLoggedDist = dist;
              lastHeartbeatLog = millis();
          }
      }
      
      if (fallDetected) {
          if (!fallConfirmed) {
              fallConfirmed = true;
              sustainedMoveStartTime = 0;
              sendBLENotification("ALERT: FALL DETECTED (Dynamic Fall Event)!\n");
          }
      } else if (isAtFloorLevel) {
          // Static floor-level presence detection (catches falls even if acoustic MIC_THUD was missed)
          if (floorLyingConsecutiveChecks == 0) {
              String warnMsg = "[WARN]: Potential Fall - Subject detected at floor level (" + String(dist) + "cm from ceiling). Monitoring...\n";
              sendBLENotification(warnMsg.c_str());
          }
          floorLyingConsecutiveChecks++;
          
          if (floorLyingConsecutiveChecks >= FLOOR_LYING_ALERT_THRESHOLD) {
              if (!fallConfirmed) {
                  fallConfirmed = true;
                  sustainedMoveStartTime = 0;
                  String alertMsg = "ALERT: FALL DETECTED (Static Floor Level Presence for >60s at " + String(dist) + "cm)!\n";
                  sendBLENotification(alertMsg.c_str());
              }
          }
      } else if (presenceDetected && dist > 0 && dist < (roomHeightCm - floorToleranceCm)) {
          // Person is standing or sitting (distance from ceiling is well above floor level)
          if (floorLyingConsecutiveChecks > 0) {
              floorLyingConsecutiveChecks = 0;
          }
          if (fallConfirmed) {
              fallConfirmed = false;
              sustainedMoveStartTime = 0;
              digitalWrite(FALL_LED_PIN, HIGH);
              String clearMsg = "[FALL] Cleared: Person stood up (height now " + String(dist) + "cm from ceiling).\n";
              sendBLENotification(clearMsg.c_str());
          }
      }

      if (fallConfirmed) {
          // Rapid flashing visual siren
          if (millis() - lastLedFlash > 250) {
              lastLedFlash = millis();
              digitalWrite(FALL_LED_PIN, !digitalRead(FALL_LED_PIN)); 
          }
          
          // Recovery check: require 5 continuous seconds of active walking movement
          bool activeMovement = (hu.smHumanData(hu.eHumanMovement) > 0); 
          if (activeMovement) {
              if (sustainedMoveStartTime == 0) {
                  sustainedMoveStartTime = millis();
              } else if (millis() - sustainedMoveStartTime > 5000) {
                  fallConfirmed = false;
                  sustainedMoveStartTime = 0;
                  digitalWrite(FALL_LED_PIN, HIGH);
                  sendBLENotification("[FALL] Cleared: Sustained movement detected (person recovered).\n");
              }
          } else {
              sustainedMoveStartTime = 0; // Lying still on floor resets recovery timer, keeping alert ACTIVE!
          }
      }
      
      // --- Trigger-Aware Smart Radar Early Exit Strategy ---
      // 1. MIC_THUD (Impact): Early exit is DISABLED. Must observe full 25s window for fall/motionless state!
      // 2. Debug Mode (Testing): 15s observation window so falls can be staged easily during test.
      // 3. PIR_WALK_IN: 8s window to observe person entering room.
      // 4. PERIODIC_TIMER (Routine Heartbeat): Fast 2.5s early exit for max battery life.
      unsigned long minObservationTime = 2500;
      bool allowEarlyExit = true;

      if (currentTrigger == MIC_THUD || isAtFloorLevel) {
          allowEarlyExit = false; // High-priority acoustic impact or subject on floor: stay on for full fall evaluation!
      } else if (debugMode) {
          minObservationTime = 15000; // 15s in debug mode for comfortable live testing
      } else if (currentTrigger == PIR_WALK_IN) {
          minObservationTime = 8000;  // 8s for walk-in verification
      } else {
          minObservationTime = 2500;  // 2.5s for routine periodic check
      }

      bool isWarm = (millis() - radarTurnedOnTime > minObservationTime);
      bool earlyExitEligible = allowEarlyExit && isWarm && presenceDetected && !fallConfirmed;
      bool snapshotTimeout = (millis() - radarTurnedOnTime > 25000);
      
      if (earlyExitEligible || snapshotTimeout) {
          String checkLabel = "Check";
          if (currentTrigger == BOOT) checkLabel = "Startup";
          else if (currentTrigger == PERIODIC_TIMER) checkLabel = "Periodic";
          else if (currentTrigger == PIR_WALK_IN) checkLabel = "PIR Walk-In";
          else if (currentTrigger == MIC_THUD) checkLabel = "MIC Thud Fall Evaluation";
          
          if (presenceDetected) {
              if (!wasOccupied) {
                  sendBLENotification("[SYS]: Person Entered.\n");
              }
              wasOccupied = true;
              String msg = earlyExitEligible 
                  ? "[SYS]: Fast Occupancy Confirmed (Early Exit at " + String(millis() - radarTurnedOnTime) + "ms). Sleeping for 60s.\n"
                  : "[SYS]: " + checkLabel + " Complete. Room occupied. Sleeping for 60s.\n";
              sendBLENotification(msg.c_str());
              goToSleep(false);  // 60s periodic sleep
          } else {
              if (pirSeenInSnapshot && micSeenInSnapshot) {
                  sendBLENotification("[WARN]: Sensor Fusion High Confidence (PIR+MIC), but Radar reports Empty!\n");
              } else if (wasOccupied) {
                  sendBLENotification("[SYS]: Person left the room.\n");
              }
              wasOccupied = false;
              String msg = "[SYS]: " + checkLabel + " Complete. Room empty. Sleeping indefinitely.\n";
              sendBLENotification(msg.c_str());
              goToSleep(true);  // Infinite sleep
          }
      }
  }
}