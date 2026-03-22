# Wiring Guide

This covers everything I needed to connect the components and get the circuit running. Most of the wiring is straightforward but the trickiest part was getting the I2C address right for the LCD and tuning the pulse threshold, both of which are explained below.

## Components Required

| Component | Quantity | Notes |
|-----------|----------|-------|
| Arduino Uno | 1 | Any Uno-compatible board works |
| LM35 Temperature Sensor | 1 | Analogue output, 10mV/°C |
| KY-039 Pulse Sensor | 1 | Or any generic finger pulse sensor module |
| 16×2 LCD with I2C backpack | 1 | I2C address is typically 0x27 or 0x3F |
| Breadboard | 1 | Half-size or larger |
| Jumper wires | ~15 | Male-to-male |
| USB cable | 1 | For power and serial logging |

---

## Wiring Table

### LM35 Temperature Sensor (TO-92 package, flat face forward)

| LM35 Pin | Arduino Pin |
|----------|-------------|
| VCC (+) | 5V |
| OUT | A0 |
| GND (–) | GND |

### KY-039 Pulse Sensor Module

| KY-039 Pin | Arduino Pin |
|------------|-------------|
| VCC | 5V |
| GND | GND |
| S (Signal) | A1 |

### I2C LCD (16×2)

| LCD Pin | Arduino Pin |
|---------|-------------|
| VCC | 5V |
| GND | GND |
| SDA | A4 |
| SCL | A5 |

---

## Notes

- **I2C address**: The sketch uses `0x27` by default. If nothing appears on the LCD, change it to `0x3F` — different manufacturers use different addresses for the same backpack.
- **Pulse sensor placement**: Rest your fingertip lightly on the sensor in a well-lit room. Pressing too hard cuts off blood flow and kills the signal entirely.
- **PULSE_THRESHOLD**: This needs tuning for your specific sensor and lighting conditions. Open the Serial Monitor, watch the raw `analogRead` values coming from A1, and set the threshold roughly halfway between the resting baseline and the peak you see when a pulse hits.
- **Power**: USB power is sufficient — the whole circuit draws well under 500mA.
