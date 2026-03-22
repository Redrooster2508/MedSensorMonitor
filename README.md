# Medical Sensor Monitor

A small embedded system that reads body temperature and heart rate, displays them live on an LCD, and logs the data for analysis on a PC.

I built this to get hands-on with biomedical sensing and embedded systems — two areas I want to develop as I go deeper into electrical engineering. It's also my first real attempt at wiring analogue sensors together with a microcontroller, so a lot of this was figuring things out as I went.

---

## What It Does

- Reads body temperature using an LM35 analogue sensor
- Detects heart rate in BPM using a KY-039 pulse sensor
- Displays both readings live on a 16×2 I2C LCD
- Streams data as CSV over USB serial for PC logging
- Includes a Python script to plot and review recorded sessions

---

## Demo

```
=== Medical Sensor Monitor ===
Time(ms), Temp(C), BPM
1002, 36.8, 0
2004, 36.9, 72
3006, 36.8, 74
```

LCD display:
```
Temp: 36.8°C
HR:   73 BPM
```

---

## Hardware

| Component | Purpose |
|-----------|---------|
| Arduino Uno | Microcontroller |
| LM35 | Analogue temperature sensor (10mV/°C) |
| KY-039 | Optical pulse sensor |
| 16×2 I2C LCD | Live display |
| Breadboard + jumper wires | Prototyping |

Full wiring and pin connections are in [`docs/wiring.md`](docs/wiring.md).

---

## Getting Started

### Upload to Arduino
- Install `LiquidCrystal_I2C` from the Arduino Library Manager
- Open `src/med_sensor_monitor.ino`
- Select your board and port, then upload

### Log Data to PC
```bash
pip install pyserial
python src/serial_logger.py --port COM3 --duration 60
```

### Plot the Data
```bash
pip install pandas matplotlib
python src/analyse.py --file log_20260101_120000.csv
```

---

## Project Structure

```
med-sensor-monitor/
├── src/
│   ├── med_sensor_monitor.ino
│   ├── serial_logger.py
│   └── analyse.py
├── docs/
│   └── wiring.md
└── README.md
```

---

## What I Learned

This project pushed me to understand things I hadn't dealt with before. A few that stood out:

- How analogue sensors work and how to convert raw voltage readings into meaningful units
- Writing a peak detection algorithm to extract BPM from a noisy analogue signal — this took more tuning than I expected
- How the I2C protocol works and why it's useful for keeping wiring clean
- Bridging Arduino and Python over serial, and building a simple data pipeline from sensor to CSV to graph

The gap between "it compiles" and "it actually works reliably" was where most of the learning happened.

---

## What I Want to Add

- [ ] SD card logging to remove the dependency on a PC
- [ ] OLED display for a sharper, more compact UI
- [ ] Moving average filter to smooth out noisy BPM readings
- [ ] Threshold alerts via buzzer for abnormal temperature or heart rate
- [ ] Bluetooth module (HC-05) for wireless data transmission

---

## About

Engineering Product Design, SUTD
Interests: Electrical Engineering · Healthcare Technology · Embedded Systems

---

*For learning purposes only — not a certified medical device.*
