"""
serial_logger.py
----------------
Connects to the Arduino over USB serial and saves the incoming sensor data
to a timestamped CSV file. I added this so I could record sessions and
analyse them properly in Python rather than just watching numbers scroll by
in the Serial Monitor.

Usage:
    python serial_logger.py --port COM3 --duration 60

Requirements:
    pip install pyserial
"""

import argparse
import csv
import serial
import time
from datetime import datetime
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Log sensor data from Arduino.")
    parser.add_argument("--port",     default="COM3",  help="Serial port (e.g. COM3 or /dev/ttyUSB0)")
    parser.add_argument("--baud",     default=9600,    type=int, help="Baud rate (default: 9600)")
    parser.add_argument("--duration", default=60,      type=int, help="Recording duration in seconds (0 = infinite)")
    return parser.parse_args()


def main():
    args = parse_args()

    output_file = Path(f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    print(f"Logging to {output_file}  |  port={args.port}  |  duration={args.duration}s")
    print("Press Ctrl+C to stop early.\n")

    start = time.time()

    with serial.Serial(args.port, args.baud, timeout=2) as ser, \
         open(output_file, "w", newline="") as f:

        writer = csv.writer(f)
        writer.writerow(["timestamp_ms", "temperature_c", "bpm"])

        # Skip header line from Arduino
        ser.readline()

        try:
            while True:
                if args.duration > 0 and (time.time() - start) > args.duration:
                    print("Duration reached — stopping.")
                    break

                line = ser.readline().decode("utf-8", errors="ignore").strip()
                if not line:
                    continue

                parts = [p.strip() for p in line.split(",")]
                if len(parts) == 3:
                    writer.writerow(parts)
                    print(f"  t={parts[0]}ms  temp={parts[1]}°C  BPM={parts[2]}")

        except KeyboardInterrupt:
            print("\nStopped by user.")

    print(f"\nData saved to {output_file}")


if __name__ == "__main__":
    main()
