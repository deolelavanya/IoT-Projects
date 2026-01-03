# IoT Telemetry System (ESP32 → Firebase → Android)

## Overview

This project demonstrates an **end-to-end IoT telemetry system** where a device publishes sensor data to a cloud backend and a mobile application consumes and visualizes that data in near real time.

The system is implemented as a **hardware-agnostic prototype**, using:
- an ESP32 device simulated in Wokwi,
- Firebase Realtime Database as the backend,
- a native Android application built with Jetpack Compose.

The architecture and communication patterns used in this project closely mirror real-world IoT systems used in automotive, consumer electronics, and fleet monitoring applications.

---

## System Architecture
+-----------------------+ +---------------------------+ +-----------------------+
| ESP32 IoT Device | ---> | Firebase Realtime Database| ---> | Android Dashboard App |
| (Wokwi Simulator) | | (Cloud Backend) | | (Jetpack Compose) |
+-----------------------+ +---------------------------+ +-----------------------+
Telemetry JSON over HTTP Visualization & Alerts
+-----------------------+ +---------------------------+ +-----------------------+
| ESP32 IoT Device | ---> | Firebase Realtime Database| ---> | Android Dashboard App |
| (Wokwi Simulator) | | (Cloud Backend) | | (Jetpack Compose) |
+-----------------------+ +---------------------------+ +-----------------------+
Telemetry JSON over HTTP Visualization & Alerts

---

## Project Structure

iot-telemetry-system/
├─ device-esp32-wokwi/
│ ├─ sketch.ino
│ └─ README.md
│
├─ IoTDashboard/
│ ├─ app/
│ ├─ gradle/
│ ├─ gradlew
│ ├─ gradlew.bat
│ ├─ build.gradle.kts
│ ├─ settings.gradle.kts


---

## Components

### 1. ESP32 Device Simulator (Wokwi)

**Location:** `device-esp32-wokwi/`

This module simulates an ESP32-based IoT device using the Wokwi online hardware simulator.

#### Functionality
- Connects to WiFi (Wokwi virtual network)
- Periodically generates telemetry data:
  - Temperature (°C)
  - Battery percentage
  - WiFi RSSI (signal strength)
  - Device ID
  - Timestamp
- Sends telemetry to Firebase using HTTP REST calls

#### Firebase Data Path
/telemetry/latest

Although simulated, the device code is structured the same way as production ESP32 firmware and can be moved to physical hardware with minimal changes.

---

### 2. Cloud Backend (Firebase Realtime Database)

Firebase acts as the central cloud backend for the system.

#### Responsibilities
- Stores the latest telemetry payload from the device
- Provides real-time data access for the Android application
- Uses a simple JSON structure for easy parsing

Firebase was selected for its real-time capabilities and simplicity, making it suitable for rapid IoT prototyping.

---

### 3. Android IoT Dashboard App

**Location:** `IoTDashboard/`

A native Android application built using **Jetpack Compose**.

#### Features
- Fetches telemetry data from Firebase
- Displays:
  - Device ID
  - Temperature
  - Battery level
  - RSSI (signal strength)
- Implements basic alert logic (e.g. high temperature warning)
- Manual refresh button
- Automatic data load on app launch

#### Technical Highlights
- Kotlin + Jetpack Compose UI
- HTTP networking using OkHttp
- JSON parsing
- Background thread for network operations
- Simple UI state management

---

## How to Run the Project

### Step 1: Run the ESP32 Simulator
1. Go to https://wokwi.com
2. Create a new **ESP32** project
3. Copy the code from:

Although simulated, the device code is structured the same way as production ESP32 firmware and can be moved to physical hardware with minimal changes.

---

### 2. Cloud Backend (Firebase Realtime Database)

Firebase acts as the central cloud backend for the system.

#### Responsibilities
- Stores the latest telemetry payload from the device
- Provides real-time data access for the Android application
- Uses a simple JSON structure for easy parsing

Firebase was selected for its real-time capabilities and simplicity, making it suitable for rapid IoT prototyping.

---

### 3. Android IoT Dashboard App

**Location:** `IoTDashboard/`

A native Android application built using **Jetpack Compose**.

#### Features
- Fetches telemetry data from Firebase
- Displays:
  - Device ID
  - Temperature
  - Battery level
  - RSSI (signal strength)
- Implements basic alert logic (e.g. high temperature warning)
- Manual refresh button
- Automatic data load on app launch

#### Technical Highlights
- Kotlin + Jetpack Compose UI
- HTTP networking using OkHttp
- JSON parsing
- Background thread for network operations
- Simple UI state management

---

## How to Run the Project

### Step 1: Run the ESP32 Simulator
1. Go to https://wokwi.com
2. Create a new **ESP32** project
3. Copy the code from:
device-esp32-wokwi/sketch.ino
4. Click **Run**
5. Confirm successful HTTP responses in the serial output

---

### Step 2: Verify Firebase Data
Open your Firebase Realtime Database and navigate to:
/telemetry/latest

You should see telemetry values updating every few seconds.

---

### Step 3: Run the Android App
1. Open `IoTDashboard/` in Android Studio
2. Allow Gradle sync to complete
3. Launch the app on an emulator or physical Android device
4. Tap **Refresh Telemetry** to fetch the latest data

---

## Continuous Integration (CI)

The Android application is built automatically using **GitHub Actions**.

### CI Pipeline
- Triggered on every push to `main`
- Sets up Java and Android SDK
- Builds a debug APK
- Uploads the APK as a downloadable artifact

This ensures the app builds reproducibly and demonstrates basic CI/CD practices for mobile development.

---

## What This Project Demonstrates

- End-to-end IoT system design
- Device-to-cloud telemetry publishing
- Cloud-hosted real-time data backend
- Android application consuming IoT data
- Practical prototyping without physical hardware
- Clean separation of device, backend, and mobile layers

---

## Notes on Hardware & Communication

This project uses a **simulated ESP32** due to hardware availability constraints.

The communication model (HTTP + JSON) and system architecture are directly transferable to:
- Physical ESP32 devices
- Gateway-based systems
- USB / serial-connected hardware via a host application

---

## Future Improvements

- Secure Firebase authentication
- Support for multiple devices
- Historical telemetry visualization
- Physical ESP32 hardware integration
- Serial / USB gateway support
- Background services on Android

---

## Author

Developed as an IoT + Android prototype project for academic and portfolio purposes.

