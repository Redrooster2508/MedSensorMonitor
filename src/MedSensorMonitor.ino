*
 * Medical Sensor Monitor
 * ----------------------
 * Reads body temperature and heart rate from two analogue sensors,
 * displays the values live on a 16x2 LCD, and streams the data over
 * serial as CSV so it can be logged and plotted on a PC.
 *
 * I built this to get hands-on with analogue sensing and I2C communication —
 * two things I kept encountering in my EE modules but hadn't actually wired up
 * myself before. Working with a noisy pulse signal in particular taught me more
 * about signal thresholding than any lecture did.
 *
 * Hardware:
 *   - Arduino Uno
 *   - LM35 temperature sensor (A0)
 *   - KY-039 pulse sensor (A1)
 *   - 16x2 I2C LCD (address 0x27)
 *
 * Author: [Your Name]
 * Date:   2026
 */

#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// ── Pin Definitions ────────────────────────────────────────────────────────
#define TEMP_PIN     A0   // LM35 temperature sensor
#define PULSE_PIN    A1   // Pulse sensor (analog)

// ── LCD Setup ──────────────────────────────────────────────────────────────
LiquidCrystal_I2C lcd(0x27, 16, 2);

// ── Heart Rate Detection ───────────────────────────────────────────────────
const int PULSE_THRESHOLD   = 550;   // Adjust based on your sensor & ambient light
const int MIN_BEAT_INTERVAL = 400;   // ms — filters noise (max ~150 BPM)

unsigned long lastBeatTime  = 0;
unsigned long beatInterval  = 0;
bool          beatDetected  = false;
int           bpm           = 0;

// ── Sampling ───────────────────────────────────────────────────────────────
unsigned long lastDisplayUpdate = 0;
const int     DISPLAY_INTERVAL  = 1000;  // refresh LCD every 1 s

// ── Temperature ────────────────────────────────────────────────────────────
float readTemperatureCelsius() {
  int raw = analogRead(TEMP_PIN);
  // The LM35 outputs 10mV per °C. With a 5V supply and 10-bit ADC (1024 steps),
  // we first convert the raw reading back to voltage, then scale to degrees.
  float voltage = raw * (5.0 / 1023.0);
  return voltage * 100.0;
}

// ── Heart Rate ─────────────────────────────────────────────────────────────
void updateHeartRate() {
  int signal = analogRead(PULSE_PIN);
  unsigned long now = millis();

  // When the signal crosses the threshold, we check that enough time has passed
  // since the last beat to filter out noise and double-detections.
  if (signal > PULSE_THRESHOLD && !beatDetected) {
    unsigned long interval = now - lastBeatTime;
    if (interval > MIN_BEAT_INTERVAL) {
      beatInterval  = interval;
      bpm           = 60000 / beatInterval;   // convert ms interval → BPM
      lastBeatTime  = now;
      beatDetected  = true;
    }
  }

  // Reset the flag once the signal drops, so we're ready for the next beat.
  if (signal < PULSE_THRESHOLD) {
    beatDetected = false;
  }
}

// ── Setup ──────────────────────────────────────────────────────────────────
void setup() {
  Serial.begin(9600);
  Serial.println("=== Medical Sensor Monitor ===");
  Serial.println("Time(ms), Temp(C), BPM");

  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Med Sensor Mon");
  lcd.setCursor(0, 1);
  lcd.print("Initialising...");
  delay(2000);
  lcd.clear();
}

// ── Main Loop ──────────────────────────────────────────────────────────────
void loop() {
  updateHeartRate();   // call frequently so we don't miss a pulse peak

  unsigned long now = millis();
  if (now - lastDisplayUpdate >= DISPLAY_INTERVAL) {
    lastDisplayUpdate = now;

    float tempC = readTemperatureCelsius();

    // ── LCD ──────────────────────────────────────────────────────────────
    lcd.setCursor(0, 0);
    lcd.print("Temp: ");
    lcd.print(tempC, 1);
    lcd.print((char)223);   // degree symbol
    lcd.print("C  ");

    lcd.setCursor(0, 1);
    lcd.print("HR:   ");
    if (bpm > 0) {
      lcd.print(bpm);
      lcd.print(" BPM   ");
    } else {
      lcd.print("-- BPM ");
    }

    // ── Serial log (CSV — easy to import into Excel / Python) ─────────
    Serial.print(now);
    Serial.print(", ");
    Serial.print(tempC, 1);
    Serial.print(", ");
    Serial.println(bpm);
  }
}
