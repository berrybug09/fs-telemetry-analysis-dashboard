import numpy as np
import pandas as pd

np.random.seed(67) #im so funny

LAP_TIME = 60
DT = 0.1
time = np.arange(0, LAP_TIME, DT)

speed = np.zeros_like(time)
throttle = np.zeros_like(time)
brake = np.zeros_like(time)
steering = np.zeros_like(time)


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
speed = np.clip(speed, 0, None)

df = pd.DataFrame({
    "Time": time,
    "Speed": speed,
    "Throttle": throttle,
    "Brake": brake,
    "Steering": steering
})

#To generate more data
# Change the values in track time enumeration & change this file name to whatever you like
df.to_csv("sample_data/sample_telemetry.csv", index=False)
print("Sample telemetry created.")