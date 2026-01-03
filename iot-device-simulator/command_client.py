import socket

HOST = "127.0.0.1"
PORT = 9001

def main():
    print(f"[client] Connecting to {HOST}:{PORT} ...")
    with socket.create_connection((HOST, PORT), timeout=5) as sock:
        hello = sock.recv(1024).decode("utf-8", errors="replace").strip()
        print("[client] Device says:", hello)
        print("[client] Type commands like: GET_INFO, GET_STATUS, SET_RATE 2, SET_MODE NORMAL, PING")
        print("[client] Type: quit to exit\n")

        while True:
            cmd = input("> ").strip()
            if cmd.lower() in {"quit", "exit"}:
                break
            sock.sendall((cmd + "\n").encode("utf-8"))
            resp = sock.recv(4096).decode("utf-8", errors="replace").strip()
            print(resp)

if __name__ == "__main__":
    main()
