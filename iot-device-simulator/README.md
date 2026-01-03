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

iot-device-simulator/
├── host_receiver.py
├── device_sim.py
├── command_client.py
└── README.md


