# IoT Device Simulator

This project is a simple IoT device simulation built to understand how IoT
devices send data, are monitored, and are controlled remotely.
It does not use physical hardware and instead focuses on communication logic
and system design.

---

## What This Project Does

- Simulates an IoT device that sends sensor data continuously
- Runs a host server that receives and monitors data from one or more devices
- Allows basic control of the device using commands (like changing sampling rate)

---

## Features

- Simulated IoT device with a unique device ID
- Continuous sensor data generation:
  - Temperature
  - Humidity
  - Battery level
  - Signal strength
- Telemetry sent as JSON messages
- Host server that:
  - Accepts multiple devices
  - Prints incoming data
  - Logs telemetry to a file
  - Detects basic health issues (high temperature, low battery, weak signal)
- Simple command interface:
  - `GET_INFO`
  - `GET_STATUS`
  - `SET_RATE <seconds>`
  - `SET_MODE <mode>`
  - `PING`

---

## Project Structure


---

## How to Run

### Requirements
- Python 3 installed

---

### Step 1: Start the Host Server
Open a terminal in this folder and run:

```bash
python host_receiver.py

