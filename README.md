# Formula Student Telemetry Dashboard

A telemetry visualization dashboard built using Python with Pandas, Streamlit and Plotly.

This started as a way to learn software development while also doing something related to Formula Student. At the moment it works with CSV telemetry files and lets you visualize driver inputs, compare drivers and stare at graphs pretending you're a race engineer.

The project currently uses generated sample telemetry data because, unfortunately, I do not have a Formula Student car parked outside my room.

From here, the goal is to slowly add more motorsport-style analysis features whenever I find free time (or whenever I decide sleep is optional).

---

## Current Features

* Telemetry CSV upload
* Speed analysis
* Throttle analysis
* Brake analysis
* Steering analysis
* Acceleration calculation
* Track map visualization
* Driver comparison
* Event detection
* Sample telemetry generation

---

## Dashboard Preview

![alt text](ss1.png)
![alt text](ss2.png)
![alt text](ss3.png)

---

## Driver Comparison

Upload two telemetry files and compare:

* Average speed
* Run duration
* Peak acceleration
* Speed traces

Perfect for proving to your teammate that they were definitely slower.
![alt text](doge.png)

---

## Current Limitations

This is not MoTeC.

The track map is currently generated using waypoint interpolation and is essentially a fancy "connect the dots" system.

Run duration is currently calculated from the telemetry timestamps and is not a true lap timer.

The generated sample data was created by a mechanical engineering student pretending to be a race engineer :P

---

## Getting It To Work

Install dependencies:

```bash
pip install -r requirements.txt
```

Launch the dashboard:

```bash
streamlit run app.py
```

The dashboard will automatically load sample telemetry if no CSV file is uploaded.

---

## Sample Data

Two sample telemetry datasets are included:

* sample_telemetry.csv
* sample_telemetry_b.csv

These are intentionally different so the driver comparison section has something interesting to show.

---


## Totally Important Technical Note

There are random references and stupid comments thrown around. Try and find them :D

---

## Thanks

To Formula Student teams around the world for making engineering unnecessarily competitive.

And to every teammate who has ever said:

> "bRo JuSt loOk at ThE teLeMEtrY."

before proceeding to explain absolutely nothing.
