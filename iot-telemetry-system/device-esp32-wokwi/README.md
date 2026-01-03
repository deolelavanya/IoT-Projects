# ESP32 Firebase Telemetry Simulator (Wokwi)

This module simulates an ESP32-based IoT device using the Wokwi online
hardware simulator.

## What it does
- Connects to WiFi (Wokwi virtual network)
- Generates telemetry data:
  - temperature
  - battery percentage
  - RSSI signal strength
- Sends data to Firebase Realtime Database every 5 seconds

## Firebase Path
/telemetry/latest

markdown
Copy code

## How to Run
1. Open https://wokwi.com
2. Create a new ESP32 project
3. Paste `sketch.ino`
4. Click **Run**

## Notes
This simulator mirrors real ESP32 behavior and can be swapped with
physical hardware with minimal changes.
