"""
server.py - Multi-threaded TCP Echo Server
------------------------------------------
Listens on a given host and port, accepts multiple client connections,
and echoes back any bytes received. Demonstrates basic socket programming
and concurrency in Python using threads.

Usage:
    python3 server.py --host 0.0.0.0 --port 5050
"""

import argparse
import socket
import threading
import sys

def handle_client(conn, addr, bufsize):
    try:
        while True:
            data = conn.recv(bufsize)
            if not data:
                break
            conn.sendall(data)  # echo back
    finally:
        conn.close()

def main():
    parser = argparse.ArgumentParser(description="TCP echo server")
    parser.add_argument("--host", default="0.0.0.0", help="Host/IP to bind (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=5050, help="Port to bind (default: 5050)")
    parser.add_argument("--bufsize", type=int, default=4096, help="Recv buffer size (default: 4096)")
    args = parser.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((args.host, args.port))
        s.listen()
        print(f"[server] listening on {args.host}:{args.port}")

        try:
            while True:
                conn, addr = s.accept()
                print(f"[server] connection from {addr}")
                t = threading.Thread(target=handle_client, args=(conn, addr, args.bufsize), daemon=True)
                t.start()
        except KeyboardInterrupt:
            print("\n[server] shutting down...")
            sys.exit(0)

if __name__ == "__main__":
    main()
