"""
client.py - TCP Echo Client
---------------------------
Connects to the echo server, sends a message, and receives the echoed
response. Also measures round-trip time (RTT) for the message.

Usage:
    python3 client.py --host 127.0.0.1 --port 5050 --message "Hello"
"""

import argparse
import socket
import time

def recv_exact(sock, n):
    """Receive exactly n bytes."""
    data = bytearray()
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            break
        data.extend(chunk)
    return bytes(data)

def benchmark(host, port, message, repeat=1000):
    """Send the same message repeatedly and measure latency + throughput."""
    payload = message.encode("utf-8")
    total_bytes = len(payload) * repeat
    latencies_ms = []

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        t0 = time.perf_counter()
        for _ in range(repeat):
            t_start = time.perf_counter()
            s.sendall(payload)
            echoed = recv_exact(s, len(payload))
            t_end = time.perf_counter()
            if echoed != payload:
                raise ValueError("Echoed message mismatch")
            latencies_ms.append((t_end - t_start) * 1000.0)
        t1 = time.perf_counter()

    avg_latency = sum(latencies_ms) / len(latencies_ms)
    p95_latency = sorted(latencies_ms)[int(0.95 * len(latencies_ms)) - 1]
    throughput_MBps = (total_bytes / (t1 - t0)) / (1024 * 1024)

    print(f"[bench] repeats: {repeat}, msg_len: {len(payload)} bytes")
    print(f"[bench] avg RTT: {avg_latency:.3f} ms, p95 RTT: {p95_latency:.3f} ms")
    print(f"[bench] throughput: {throughput_MBps:.2f} MB/s")

def main():
    parser = argparse.ArgumentParser(description="TCP echo client")
    parser.add_argument("--host", default="127.0.0.1", help="Server host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=5050, help="Server port (default: 5050)")
    parser.add_argument("--message", default="Hello, AWS!", help='Message to send (default: "Hello, AWS!")')
    parser.add_argument("--bench", action="store_true", help="Run benchmark mode instead of single message")
    parser.add_argument("--repeat", type=int, default=1000, help="Number of messages in benchmark mode (default: 1000)")
    parser.add_argument("--parallel", type=int, default=1, help="Number of parallel clients for benchmark mode")
    args = parser.parse_args()

    if args.bench:
        if args.parallel == 1:
            benchmark(args.host, args.port, args.message, repeat=args.repeat)
        else:
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor(max_workers=args.parallel) as pool:
                futures = [
                    pool.submit(benchmark, args.host, args.port, args.message, args.repeat)
                    for _ in range(args.parallel)
                ]
                for f in futures:
                    f.result()
        return


    payload = args.message.encode("utf-8")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((args.host, args.port))
        t0 = time.perf_counter()
        s.sendall(payload)
        echoed = recv_exact(s, len(payload))
        t1 = time.perf_counter()

    rtt_ms = (t1 - t0) * 1000.0
    print(f"[client] sent    : {payload!r}")
    print(f"[client] received: {echoed!r}")
    print(f"[client] RTT     : {rtt_ms:.3f} ms")

if __name__ == "__main__":
    main()
