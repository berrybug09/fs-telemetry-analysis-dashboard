import pandas as pd
import numpy as np

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
        "Track Length (m)": df["Distance"].max(),
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


def distance(df):
    dx = df["GPS_X"].diff().fillna(0)
    dy = df["GPS_Y"].diff().fillna(0)
    segment_distance = np.sqrt(dx**2 + dy**2)
    df["Distance"] = segment_distance.cumsum()
    return df


def track_cd(track_df):
    track_df = track_df.copy()
    dx = track_df["x_m"].diff()
    dy = track_df["y_m"].diff()
    heading = np.arctan2(dy, dx)
    heading_change = np.abs(np.arctan2(np.sin(heading.diff()), np.cos(heading.diff()))    )
    track_df["Heading_Change"] = heading_change
    return track_df
    

def track_corner_detection(track_df):
    corner_threshold = 0.05
    corner_mask = track_df["Heading_Change"] > corner_threshold
    corners = []
    in_corner = False
    for i in range(len(track_df)):
        if corner_mask.iloc[i] and not in_corner:
            start = i
            in_corner = True

        elif not corner_mask.iloc[i] and in_corner:
            end = i - 1
            corners.append((start, end))
            in_corner = False
    
    merged = []
    for start, end in corners:
        if not merged:
            merged.append([start, end])

        else:
            prev_start, prev_end = merged[-1]

            if start - prev_end <= 10:
                merged[-1][1] = end
            else:
                merged.append([start, end])
    return merged


def track_to_telemetry_corners(track_corners, track_df, df):
    telemetry_corners = []
    for start, end in track_corners:
        tele_start = int(start * len(df) / len(track_df))
        tele_end = int(end * len(df) / len(track_df))
        telemetry_corners.append((tele_start, tele_end))
    return telemetry_corners


def corner_analysis_from_track(df, telemetry_corners):
    results = []
    for i, (start, end) in enumerate(telemetry_corners, start=1):
        corner_df = df.iloc[start:end+1]
        entry_speed = corner_df["Speed"].iloc[0]
        apex_speed = corner_df["Speed"].min()
        exit_speed = corner_df["Speed"].iloc[-1]
        corner_time = (corner_df["Time"].iloc[-1] - corner_df["Time"].iloc[0])
        results.append({
            "Corner": i,
            "Entry Speed": round(entry_speed, 1),
            "Apex Speed": round(apex_speed, 1),
            "Exit Speed": round(exit_speed, 1),
            "Corner Time": round(corner_time, 2)
        })
    return pd.DataFrame(results)