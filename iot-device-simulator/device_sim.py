import json
import random
import socket
import sys
import threading
import time
from datetime import datetime, timezone

HOST = "127.0.0.1"
TELEMETRY_PORT = 9000
COMMAND_PORT = 9001

DEVICE_ID = sys.argv[1] if len(sys.argv) > 1 else "DEV_001"

# Device state (OEM-ish)
state = {
    "sampling_rate_sec": 1.0,
    "firmware": "1.0.0-sim",
    "mode": "NORMAL",
    "last_error": 0,
}
state_lock = threading.Lock()


def make_telemetry():
    temperature = round(random.uniform(22.0, 30.0), 2)
    humidity = round(random.uniform(35.0, 70.0), 2)
    battery = random.randint(40, 100)
    rssi = random.randint(-90, -45)

    with state_lock:
        sampling_rate = state["sampling_rate_sec"]
        mode = state["mode"]

    return {
        "device_id": DEVICE_ID,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "temperature_c": temperature,
        "humidity_pct": humidity,
        "battery_pct": battery,
        "rssi_dbm": rssi,
        "mode": mode,
        "status": "OK",
        "sampling_rate_sec": sampling_rate,
    }


def telemetry_loop():
    print(f"[device {DEVICE_ID}] Telemetry connecting to {HOST}:{TELEMETRY_PORT} ...")
    while True:
        try:
            with socket.create_connection((HOST, TELEMETRY_PORT), timeout=5) as sock:
                print(f"[device {DEVICE_ID}] Telemetry connected ✅ streaming...")
                while True:
                    msg = make_telemetry()
                    sock.sendall((json.dumps(msg) + "\n").encode("utf-8"))

                    with state_lock:
                        rate = state["sampling_rate_sec"]
                    time.sleep(rate)

        except (ConnectionRefusedError, OSError) as e:
            print(f"[device {DEVICE_ID}] Telemetry host not ready ({e}). Retrying in 1s...")
            time.sleep(1)


def handle_command(conn: socket.socket, addr):
    conn.sendall(f"HELLO {DEVICE_ID}\n".encode("utf-8"))
    buffer = ""
    while True:
        data = conn.recv(4096)
        if not data:
            break
        buffer += data.decode("utf-8", errors="replace")
        while "\n" in buffer:
            line, buffer = buffer.split("\n", 1)
            cmd = line.strip()
            if not cmd:
                continue

            parts = cmd.split()
            op = parts[0].upper()

            if op == "GET_INFO":
                with state_lock:
                    fw = state["firmware"]
                resp = {"device_id": DEVICE_ID, "firmware": fw, "type": "sim-iot-node"}
                conn.sendall((json.dumps(resp) + "\n").encode("utf-8"))

            elif op == "GET_STATUS":
                with state_lock:
                    resp = {
                        "device_id": DEVICE_ID,
                        "mode": state["mode"],
                        "sampling_rate_sec": state["sampling_rate_sec"],
                        "last_error": state["last_error"],
                    }
                conn.sendall((json.dumps(resp) + "\n").encode("utf-8"))

            elif op == "SET_RATE" and len(parts) == 2:
                try:
                    new_rate = float(parts[1])
                    if new_rate <= 0:
                        raise ValueError("rate must be > 0")
                    with state_lock:
                        state["sampling_rate_sec"] = new_rate
                    conn.sendall(f"OK sampling_rate_sec={new_rate}\n".encode("utf-8"))
                except ValueError:
                    conn.sendall(b"ERR invalid_rate\n")

            elif op == "SET_MODE" and len(parts) == 2:
                new_mode = parts[1].upper()
                with state_lock:
                    state["mode"] = new_mode
                conn.sendall(f"OK mode={new_mode}\n".encode("utf-8"))

            elif op == "PING":
                conn.sendall(b"PONG\n")

            else:
                conn.sendall(b"ERR unknown_command\n")


def command_server():
    print(f"[device {DEVICE_ID}] Command server listening on 127.0.0.1:{COMMAND_PORT}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("127.0.0.1", COMMAND_PORT))
        server.listen(5)
        while True:
            conn, addr = server.accept()
            print(f"[device {DEVICE_ID}] Command client connected from {addr} ✅")
            with conn:
                handle_command(conn, addr)
            print(f"[device {DEVICE_ID}] Command client disconnected.")


def main():
    print(f"[device {DEVICE_ID}] Starting simulator")
    t1 = threading.Thread(target=telemetry_loop, daemon=True)
    t2 = threading.Thread(target=command_server, daemon=True)
    t1.start()
    t2.start()

    # Keep main alive
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
