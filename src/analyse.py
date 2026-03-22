"""
analyse.py
----------
Loads a logged CSV file and plots temperature and heart rate over time.
Writing this helped me understand how to go from raw serial data to something
you can actually read and draw conclusions from — pandas for the data wrangling,
matplotlib for the visualisation.

Usage:
    python analyse.py --file log_20260101_120000.csv

Requirements:
    pip install pandas matplotlib
"""

import argparse
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Analyse and plot sensor log.")
    parser.add_argument("--file", required=True, help="Path to CSV log file")
    return parser.parse_args()


def main():
    args = parse_args()
    path = Path(args.file)

    df = pd.read_csv(path)
    df.columns = ["timestamp_ms", "temperature_c", "bpm"]
    df["time_s"] = df["timestamp_ms"] / 1000.0

    # Zero BPM means no beat was detected yet — filter those rows out before plotting
    df_bpm = df[df["bpm"] > 0]

    print(f"\n── Summary ({path.name}) ──────────────────────")
    print(f"  Duration      : {df['time_s'].max():.1f} s")
    print(f"  Temp  mean    : {df['temperature_c'].mean():.1f} °C")
    print(f"  Temp  range   : {df['temperature_c'].min():.1f} – {df['temperature_c'].max():.1f} °C")
    if not df_bpm.empty:
        print(f"  BPM   mean    : {df_bpm['bpm'].mean():.0f}")
        print(f"  BPM   range   : {df_bpm['bpm'].min()} – {df_bpm['bpm'].max()}")
    print()

    fig = plt.figure(figsize=(10, 6))
    fig.suptitle(f"Medical Sensor Monitor — {path.stem}", fontsize=13, fontweight="bold")
    gs = gridspec.GridSpec(2, 1, hspace=0.45)

    ax1 = fig.add_subplot(gs[0])
    ax1.plot(df["time_s"], df["temperature_c"], color="#e05c5c", linewidth=1.8)
    ax1.set_ylabel("Temperature (°C)")
    ax1.set_xlabel("Time (s)")
    ax1.set_title("Body Temperature")
    ax1.grid(True, alpha=0.3)
    ax1.axhline(37.0, color="grey", linestyle="--", linewidth=0.8, label="Normal 37°C")
    ax1.legend(fontsize=8)

    ax2 = fig.add_subplot(gs[1])
    if not df_bpm.empty:
        ax2.plot(df_bpm["time_s"], df_bpm["bpm"], color="#5
