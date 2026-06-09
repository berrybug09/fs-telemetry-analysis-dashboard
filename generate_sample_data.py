import numpy as np
import pandas as pd

np.random.seed(67) #im so funny

time = np.arange(0, 60, 0.1)

speed = np.zeros_like(time)
throttle = np.zeros_like(time)
brake = np.zeros_like(time)
steering = np.zeros_like(time)
gps_x = np.zeros_like(time)
gps_y = np.zeros_like(time)


#For this track, every speed starting point is based on the previous cutoff
for i, t in enumerate(time):

    # Straight 1
    if t < 10:
        speed[i] = 10 * t
        throttle[i] = 100
        steering[i] = np.random.normal(0, 1)

    # Corner 1
    elif t < 15:
        speed[i] = 100 - 8 * (t - 10)
        throttle[i] = 20
        brake[i] = 70
        steering[i] = 25

    # Straight 2
    elif t < 25:
        speed[i] = 60 + 4 * (t - 15)
        throttle[i] = 100
        steering[i] = np.random.normal(0, 1)

    # Hairpin
    elif t < 30:
        speed[i] = 100 - 10 * (t - 25)
        throttle[i] = 10
        brake[i] = 100
        steering[i] = -35

    # Straight 3
    elif t < 40:
        speed[i] = 50 + 5 * (t - 30)
        throttle[i] = 100
        steering[i] = np.random.normal(0, 1)

    # Chicane
    elif t < 50:
        speed[i] = 100 - 2 * np.sin((t - 40) * 2)
        throttle[i] = 60
        steering[i] = 20 * np.sin((t - 40) * 2)

    # Final corner
    else:
        speed[i] = 100 - 4 * (t - 50)
        throttle[i] = 30
        brake[i] = 50
        steering[i] = 18

speed += np.random.normal(0, 1.5, len(speed))


#TRACK
# TODO -  make track less potato shaped :D
track_points = np.array([
    [0, 0],      # Go
    [100, 0],    # Full send straight
    [140, 40],   # Sweeper
    [140, 120],  # Hairpin entry
    [80, 180],   # Hairpin exit
    [20, 150],   # Back section
    [-20, 100],  # Chicane entry
    [20, 60],    # Chicane middle
    [-20, 20],   # Chicane exit
    [0, 0]       # Fin
])

segment_lengths = np.sqrt(np.sum(np.diff(track_points, axis=0)**2, axis=1))
cumulative_length = np.concatenate(([0], np.cumsum(segment_lengths)))

total_length = cumulative_length[-1]

sample_distance = np.linspace(0, total_length, len(time))

gps_x = np.interp(sample_distance, cumulative_length, track_points[:, 0])

gps_y = np.interp(sample_distance, cumulative_length, track_points[:, 1])

df = pd.DataFrame({
    "Time": time,
    "Speed": speed,
    "Throttle": throttle,
    "Brake": brake,
    "Steering": steering,
    "GPS_X": gps_x,
    "GPS_Y": gps_y
})


df.to_csv("sample_data/sample_telemetry_b.csv", index=False)
print("Sample telemetry created.")