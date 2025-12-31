import json
import socket
import threading
import time
from datetime import datetime

HOST = "127.0.0.1"
PORT = 9000

LOG_FILE = "telemetry.log"

# Thresholds
MAX_TEMP_C = 28.5
MIN_BATTERY_PCT = 50
MIN_RSSI_DBM = -80

SUMMARY_EVERY_SEC = 30

# Lock for file writes (so multiple threads don't interleave writes)
log_lock = threading.Lock()


def pretty_print(msg: dict):
    ts = msg.get("timestamp", "?")
    did = msg.get("device_id", "?")
    temp = msg.get("temperature_c", "?")
    hum = msg.get("humidity_pct", "?")
    batt = msg.get("battery_pct", "?")
    rssi = msg.get("rssi_dbm", "?")
    status = msg.get("status", "?")

    print(f"[{did}] {ts} | temp={temp}C hum={hum}% batt={batt}% rssi={rssi}dBm status={status}")


def validate(msg: dict) -> bool:
    required = ["device_id", "timestamp", "temperature_c", "humidity_pct"]
    return all(k in msg for k in required)


def check_alerts(msg: dict):
    alerts = []
    did = msg.get("device_id", "UNKNOWN")

    temp = msg.get("temperature_c")
    batt = msg.get("battery_pct")
    rssi = msg.get("rssi_dbm")

    if isinstance(temp, (int, float)) and temp > MAX_TEMP_C:
        alerts.append(f"HIGH_TEMP ({temp}C > {MAX_TEMP_C}C)")
    if isinstance(batt, int) and batt < MIN_BATTERY_PCT:
        alerts.append(f"LOW_BATTERY ({batt}% < {MIN_BATTERY_PCT}%)")
    if isinstance(rssi, int) and rssi < MIN_RSSI_DBM:
        alerts.append(f"WEAK_SIGNAL ({rssi}dBm < {MIN_RSSI_DBM}dBm)")

    if alerts:
        print(f"[ALERT] {did}: " + " | ".join(alerts))


def append_log(entry: dict):
    line = json.dumps(entry)
    with log_lock:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")


def handle_device(conn: socket.socket, addr, client_id: int):
    print(f"[host] Device #{client_id} connected from {addr}")
    buffer = ""

    stats = {
        "count": 0,
        "temp_sum": 0.0,
        "temp_min": float("inf"),
        "temp_max": float("-inf"),
        "window_start": time.time(),
        "device_id": f"UNKNOWN_{client_id}",
    }

    try:
        while True:
            data = conn.recv(4096)
            if not data:
                print(f"[host] Device #{client_id} disconnected.")
                break

            buffer += data.decode("utf-8", errors="replace")

            # Periodic per-device summary
            now = time.time()
            if now - stats["window_start"] >= SUMMARY_EVERY_SEC and stats["count"] > 0:
                avg_temp = stats["temp_sum"] / stats["count"]
                print(
                    f"[SUMMARY {stats['device_id']} last {SUMMARY_EVERY_SEC}s] "
                    f"msgs={stats['count']} "
                    f"temp_avg={avg_temp:.2f}C "
                    f"temp_min={stats['temp_min']:.2f}C "
                    f"temp_max={stats['temp_max']:.2f}C"
                )
                stats = {
                    "count": 0,
                    "temp_sum": 0.0,
                    "temp_min": float("inf"),
                    "temp_max": float("-inf"),
                    "window_start": now,
                    "device_id": stats["device_id"],
                }

            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                line = line.strip()
                if not line:
                    continue

                try:
                    msg = json.loads(line)
                except json.JSONDecodeError:
                    print(f"[host] Warning: Device #{client_id} invalid JSON:", line[:120])
                    continue

                if not validate(msg):
                    print(f"[host] Warning: Device #{client_id} missing fields:", msg)
                    continue

                # Update known device_id
                if isinstance(msg.get("device_id"), str):
                    stats["device_id"] = msg["device_id"]

                pretty_print(msg)
                check_alerts(msg)

                # Update stats
                temp = msg.get("temperature_c")
                if isinstance(temp, (int, float)):
                    stats["count"] += 1
                    stats["temp_sum"] += float(temp)
                    stats["temp_min"] = min(stats["temp_min"], float(temp))
                    stats["temp_max"] = max(stats["temp_max"], float(temp))

                entry = {
                    "received_at": datetime.utcnow().isoformat() + "Z",
                    "source_addr": f"{addr[0]}:{addr[1]}",
                    "telemetry": msg,
                }
                append_log(entry)

    finally:
        conn.close()


def main():
    print(f"[host] Multi-device listener on {HOST}:{PORT}")
    print(f"[host] Logging to {LOG_FILE}")
    print(
        f"[host] Thresholds: MAX_TEMP_C={MAX_TEMP_C}, MIN_BATTERY_PCT={MIN_BATTERY_PCT}, MIN_RSSI_DBM={MIN_RSSI_DBM}"
    )

    client_counter = 0

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(10)

        while True:
            conn, addr = server.accept()
            client_counter += 1
            t = threading.Thread(
                target=handle_device,
                args=(conn, addr, client_counter),
                daemon=True,
            )
            t.start()


if __name__ == "__main__":
    main()

