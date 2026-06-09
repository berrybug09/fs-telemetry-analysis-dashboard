import pandas as pd

def load_data(file):
    return pd.read_csv(file)

def calc(df):
    metrics = {
        "Max Speed (km/h)": df["Speed"].max(),
        "Average Speed (km/h)": df["Speed"].mean(),
        "Lap Duration (s)": df["Time"].max() - df["Time"].min(),
        "Peak Acceleration": df["Acceleration"].max(),
        "Peak Deceleration": df["Acceleration"].min(),
        "Average Throttle (%)": df["Throttle"].mean(),
        "Brake Usage (%)": (df["Brake"] > 0).mean() * 100,
    }
    return metrics

def braking(df):
    return df[df["Brake"] > 10]

def full_send(df): #full send for a grandma wagon
    return df[df["Throttle"] > 20]

def xlr8(df): #yes, ben10 homage because peak
    speed_ms = df["Speed"] / 3.6 #otherwise acceleration units become km/h/s :D
    df["Acceleration"] = (speed_ms.diff() / df["Time"].diff())
    return df