import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

from telemetry_analysis import (calc, braking, full_send, xlr8, distance, track_cd, track_corner_detection, track_to_telemetry_corners, corner_analysis_from_track)

st.set_page_config(page_title="Telemetry Analysis Dashboard", layout="wide")

st.title("🏎️ Formula Student Telemetry Dashboard")

st.divider()

track_files = [f for f in os.listdir("tracks") if f.endswith(".csv")]
selected_track = st.selectbox("Select Track", track_files)

#For user input; enter sample data, else will use pre-generated data
uploaded_file = st.file_uploader("Upload Telemetry CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("sample_data/sample_telemetry.csv")

df = xlr8(df)
track_df = pd.read_csv(f"tracks/{selected_track}")
track_df.columns = track_df.columns.str.replace("# ", "")
track_indices = np.linspace(0, len(track_df) - 1, len(df)).astype(int)
df["GPS_X"] = track_df["x_m"].iloc[track_indices].values
df["GPS_Y"] = track_df["y_m"].iloc[track_indices].values
df = distance(df)

with st.expander("View Raw Telemetry Data"):
    st.dataframe(df)

# KPIs
metrics = calc(df)
st.subheader("Lap Summary")
cols = st.columns(len(metrics))
for col, (name, value) in zip(cols, metrics.items()):
    col.metric(name, f"{value:.2f}")

# Speed plot
st.subheader("Speed vs Time")
fig_speed = px.line(df, x="Time", y="Speed")
st.plotly_chart(fig_speed, use_container_width=True)

# Throttle plot
st.subheader("Throttle vs Time")
fig_throttle = px.line(df, x="Time", y="Throttle")
st.plotly_chart(fig_throttle, use_container_width=True)

# Brake plot
st.subheader("Brake vs Time")
fig_brake = px.line(df, x="Time", y="Brake")
st.plotly_chart(fig_brake, use_container_width=True)

# Steering plot
st.subheader("Steering vs Time")
fig_steering = px.line(df, x="Time", y="Steering")
st.plotly_chart(fig_steering, use_container_width=True)

# Acceleration plot
st.subheader("Acceleration vs Time")
fig_accel = px.line(df, x="Time", y="Acceleration")
st.plotly_chart(fig_accel, use_container_width=True)


# Event detection
braking_events = braking(df)
acceleration_events = full_send(df)
st.subheader("Detected Events")
col1, col2 = st.columns(2)
col1.metric("Braking Samples", len(braking_events))
col2.metric("Acceleration Samples", len(acceleration_events))


# TRACK
track_df = track_cd(track_df)
fig_track = go.Figure()
fig_track.add_trace(go.Scatter(x=track_df["x_m"], y=track_df["y_m"], mode="lines", name="Track"))
track_corners = track_corner_detection(track_df)
telemetry_corners = track_to_telemetry_corners(track_corners, track_df, df)
for i, (start, end) in enumerate(track_corners, start=1):
    corner_section = track_df.iloc[start:end+1]
    corner_idx = corner_section["Heading_Change"].idxmax()
    fig_track.add_trace(go.Scatter(x=[track_df["x_m"].iloc[corner_idx]], y=[track_df["y_m"].iloc[corner_idx]], showlegend=False, mode="markers+text", text=[f"C{i}"], textposition="top center", name=f"Corner {i}"))
fig_track.update_yaxes(scaleanchor="x", scaleratio=1)
st.subheader("Track Map")
st.plotly_chart(fig_track, use_container_width=True)


# Corner Analysis
corner_results = corner_analysis_from_track(df, telemetry_corners)
st.subheader("Corner Analysis")
st.dataframe(corner_results, hide_index=True, width="stretch")


# DRIVER COMPARISON
st.header("Driver Comparison")
driver_a = st.file_uploader("Upload Driver A CSV", type=["csv"], key="driver_a")
driver_b = st.file_uploader("Upload Driver B CSV", type=["csv"], key="driver_b")

if driver_a is not None and driver_b is not None:
    df_a = pd.read_csv(driver_a)
    df_b = pd.read_csv(driver_b)

    df_a = xlr8(df_a)
    df_b = xlr8(df_b)

    st.subheader("Driver Comparison KPIs")
    col1, col2 = st.columns(2)
    with col1:
        st.write("### Driver A")
        st.metric("Average Speed", f"{df_a['Speed'].mean():.2f}")
        st.metric("Run Time (s)", f"{df_a['Time'].max() - df_a['Time'].min():.2f}")
        st.metric("Peak Acceleration", f"{df_a['Acceleration'].max():.2f}")

    with col2:
        st.write("### Driver B")
        st.metric("Average Speed", f"{df_b['Speed'].mean():.2f}")
        st.metric("Run Time (s)", f"{df_b['Time'].max() - df_b['Time'].min():.2f}")
        st.metric("Peak Acceleration", f"{df_b['Acceleration'].max():.2f}")

    st.subheader("Speed Comparison")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_a["Time"], y=df_a["Speed"], name="Driver A"))
    fig.add_trace(go.Scatter(x=df_b["Time"], y=df_b["Speed"], name="Driver B"))

    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Upload Driver A and Driver B CSV files to enable comparison")