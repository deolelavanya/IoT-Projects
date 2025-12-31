# IoT Device Simulator

This project is a simple simulation of an IoT device and a host system.
It demonstrates how IoT devices send telemetry data, how servers receive and
monitor that data, and how basic remote commands can control a device.

The project does not use physical hardware and focuses on learning IoT
communication and monitoring concepts.

---

## Features

- Simulated IoT device with a unique device ID
- Continuous telemetry generation (temperature, humidity, battery, signal strength)
- Telemetry sent in JSON format
- Host server that:
  - Accepts multiple devices simultaneously
  - Prints and logs telemetry data
  - Detects basic device health issues
- Command interface to control and inspect the device

---

## Project Structure

project-1-telemetry/
├── host_receiver.py
├── device_sim.py
├── command_client.py
└── README.md

yaml
Copy code

---

## How to Run

### Requirements
- Python 3 installed

---

### Step 1: Start the Host Server

Open a terminal in this folder and run:

```bash
python host_receiver.py
Step 2: Start the IoT Device
Open a new terminal and run:

bash
Copy code
python device_sim.py DEV_001
You can simulate multiple devices by running the following in separate terminals:

bash
Copy code
python device_sim.py DEV_002
bash
Copy code
python device_sim.py DEV_003
Step 3: Send Commands to the Device
Open another terminal and run:

bash
Copy code
python command_client.py
You can then send commands such as:

text
Copy code
GET_INFO
GET_STATUS
SET_RATE 2
SET_MODE TEST
PING
Output
Telemetry data is printed in the host terminal

All telemetry data is logged to telemetry.log

Alerts are shown if device health thresholds are exceeded

Notes
This project is intended for learning and experimentation.
The architecture can be extended to work with real IoT hardware
using serial or USB communication.
