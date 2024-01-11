import datetime
from datetime import datetime as dt
import json

import matplotlib.pyplot as plt
from collections import deque
import time

# Sample data
with open("data.json", "r") as f:
    entries = json.load(f)
    entries: list[dict[str,int]]

# Keep only the last 30 entries
entries = deque(entries, maxlen=30)

# Extract data for plotting
timestamps = [dt.fromtimestamp(entry["timestamp"]).strftime("%H:%M:%S") for entry in entries]
trophies = [entry["trophies"] for entry in entries]
modes = [entry["mode"] for entry in entries]

# Plotting trophies
plt.figure(figsize=(10, 6),dpi=500)
plt.plot(timestamps, trophies, label='Trophies', marker='o', linestyle='-', color='blue')

# Plotting mode
for mode_val, trophy_val, timestamp_val in zip(modes, trophies, timestamps):
    plt.text(timestamp_val, trophy_val, f'Mode {mode_val}', fontsize=8, ha='right', va='bottom')

# Customize the plot
plt.title('Trophies and Mode Over Time')
plt.xlabel('Timestamp')
plt.ylabel('Trophies')
plt.legend()
plt.grid(True)

# Show the plot
plt.savefig('trophies_and_mode_plot.png', dpi=300)  # Adjust dpi as needed
plt.show()
