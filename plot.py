import datetime
from datetime import datetime as dt
import json

import matplotlib.pyplot as plt
from collections import deque
import time

import requests


while True:
    #get data from http://192.168.178.62:5000/data
    response = requests.get("http://192.168.178.62:5000/data?max_age=60")
    entries = response.json()

    # Extract data for plotting
    timestamps = [dt.fromtimestamp(entry["timestamp"]).strftime("%H:%M:%S") for entry in entries]
    trophies = [entry["trophies"] for entry in entries]
    modes = [entry["mode"] for entry in entries]

    max_trophy_jump = 200
    filtered_timestamps = [timestamps[0]]
    filtered_trophies = [trophies[0]]
    filtered_modes = [modes[0]]

    for timestamp, trophy, mode in zip(timestamps[1:], trophies[1:], modes[1:]):
        trophy_jump = abs(trophy - filtered_trophies[-1])
        if trophy_jump <= max_trophy_jump:
            filtered_timestamps.append(timestamp)
            filtered_trophies.append(trophy)
            filtered_modes.append(mode)

    segments = []
    last_change = filtered_timestamps[0]
    current_mode = filtered_modes[0]
    for i in range(1, len(filtered_modes)):
        if filtered_modes[i] != current_mode:
            segments.append((last_change, filtered_timestamps[i], current_mode))
            current_mode = filtered_modes[i]
            last_change = filtered_timestamps[i]

    # Append the last segment
    segments.append((last_change, timestamps[-1], current_mode))

    # Plotting trophies
    plt.figure(figsize=(10, 6), dpi=500)
    plt.plot(filtered_timestamps, filtered_trophies, label='Trophies', marker='o',markersize=2, linestyle='-', color='blue')
    for start, end, mode in segments:
        color = 'green' if mode == 1 else 'red'  # Change 'mode1' to the actual mode name
        plt.axvspan(start, end, facecolor=color, alpha=0.3)


    """
    # Plotting mode with improved positioning
    for mode_val, trophy_val, timestamp_val in zip(filtered_modes, filtered_trophies, filtered_timestamps):
        annotation_position = (timestamp_val, trophy_val)
        textcoords = "offset points"
        xytext = (10, 0)
        va = 'top' if trophy_val > max(filtered_trophies) - 5 else 'bottom'
        va = 'top'
    
        plt.annotate(f'Mode {mode_val}', annotation_position, textcoords=textcoords, xytext=xytext,
                     ha='right', fontsize=8, va=va, rotation=30)
    """
    # Customize the plot
    plt.title('Trophies and Mode Over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Trophies')
    legend_labels = ["Drop", "Attack"]  # Adjust the labels based on your modes
    legend_handles = [plt.Rectangle((0, 0), 1, 1, fc='green', alpha=0.3),
                      plt.Rectangle((0, 0), 1, 1, fc='red', alpha=0.3)]

    plt.legend(legend_handles, legend_labels)

    plt.grid(True)

    # Set x-axis ticks at intervals (e.g., every 5 entries)
    interval = len(filtered_timestamps) // 20
    plt.xticks(filtered_timestamps[::interval])
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability

    # Show the plot
    plt.savefig('trophies_and_mode_plot.png', dpi=700)  # Adjust dpi as needed
    plt.show()
    time.sleep(40)