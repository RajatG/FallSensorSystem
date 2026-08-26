// ATtiny85 MIC Debug Firmware
// PURPOSE: Flash MIC_OUT (PB0) LED to visually confirm whether the ATtiny85
//          is seeing the MIC's digital output transitions.
//
// WIRING FOR DEBUG:
//   Connect an LED + 330Ω resistor from PB0 (MIC_OUT_PIN) to GND.
//   Or just observe the ESP32's Pin 4 line — it will pulse on every MIC detection.
//
// BEHAVIOR:
//   - On MIC state change: 3 rapid blinks (100ms each) on PB0
//   - On PIR trigger: 1 long blink (500ms) on PB2 (normal)
//   - Between triggers: PB3 (onboard LED on some Digispark boards) shows MIC_IN raw state
//
// After debugging, reflash with the production fall_attiny_v1.ino

#include <avr/sleep.h>
#include <avr/interrupt.h>

// --- HARDWARE PINS ---
#define MIC_OUT_PIN  0  // PB0: Sends wake pulse to ESP32 Pin 4
#define PIR_IN_PIN   1  // PB1: PCINT1 (From PIR module)
#define PIR_OUT_PIN  2  // PB2: Sends wake pulse to ESP32 Pin 13
#define LED_DBG_PIN  3  // PB3: Onboard LED (Digispark Model B) — used as MIC level mirror
#define MIC_IN_PIN   4  // PB4: PCINT4 (From 4-Pin Mic DO pin)

bool lastPirState = LOW;
bool lastMicState = LOW;
volatile bool wakeFlag = false;

ISR(PCINT0_vect) {
  wakeFlag = true;
}

void blinkFast(int pin, int count) {
  for (int i = 0; i < count; i++) {
    digitalWrite(pin, HIGH);
    delay(100);
    digitalWrite(pin, LOW);
    delay(100);
  }
}

void setup() {
  pinMode(PIR_OUT_PIN, OUTPUT);
  pinMode(MIC_OUT_PIN, OUTPUT);
  pinMode(LED_DBG_PIN, OUTPUT);  // Debug LED
  
  digitalWrite(PIR_OUT_PIN, LOW);
  digitalWrite(MIC_OUT_PIN, LOW);
  digitalWrite(LED_DBG_PIN, LOW);

  pinMode(PIR_IN_PIN, INPUT);
  pinMode(MIC_IN_PIN, INPUT_PULLUP);  // Same as production: internal pull-up for clean idle HIGH

  // Configure Pin Change Interrupts for PIR and MIC
  GIMSK |= (1 << PCIE);    
  PCMSK |= (1 << PCINT1);  // PIR
  PCMSK |= (1 << PCINT4);  // MIC

  set_sleep_mode(SLEEP_MODE_PWR_DOWN);
  
  // Startup blink: 5 rapid flashes on MIC_OUT to confirm firmware is loaded
  blinkFast(MIC_OUT_PIN, 5);
}

void loop() {
  bool currentPirState = digitalRead(PIR_IN_PIN);
  bool currentMicState = digitalRead(MIC_IN_PIN);

  // --- Mirror MIC_IN raw level to debug LED ---
  // This lets you see the LIVE state of the MIC digital output
  // If the LED stays solid ON or solid OFF and never changes during sound,
  // the MIC module's HIGH isn't crossing ATtiny85's VIH threshold (~2.6V @ 5V VCC)
  digitalWrite(LED_DBG_PIN, currentMicState);

  // --- PIR LOGIC (normal) ---
  if (currentPirState == HIGH && lastPirState == LOW) {
    digitalWrite(PIR_OUT_PIN, HIGH);
    delay(50); 
    digitalWrite(PIR_OUT_PIN, LOW);
  } 
  
  // --- MIC LOGIC (debug enhanced) ---
  if (currentMicState != lastMicState) {
    // Normal wake pulse to ESP32
    digitalWrite(MIC_OUT_PIN, HIGH);
    delay(50);
    digitalWrite(MIC_OUT_PIN, LOW);
    
    // DEBUG: 3 rapid blinks on MIC_OUT to visually confirm detection
    delay(100);
    blinkFast(MIC_OUT_PIN, 3);
    
    // 500ms acoustic debounce
    delay(500); 
  }

  lastPirState = currentPirState;
  lastMicState = digitalRead(MIC_IN_PIN); 

  // --- SLEEP ---
  sleep_enable();
  noInterrupts();
  GIFR = (1 << PCIF); 
  interrupts();
  sleep_cpu();
  sleep_disable();
}
