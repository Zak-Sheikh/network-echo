# Simple TCP Echo (Python)

A minimal TCP echo server and client built with Python sockets.  
This project demonstrates the fundamentals of **socket programming**,  
**concurrent servers**, and **latency measurement** — key systems concepts.

---

## Features

- **Echo server**: multi-threaded, handles multiple clients concurrently.
- **Client**: sends a message, waits for response, measures round-trip latency (RTT).
- **Configurable**: host, port, buffer size, and message text.
- **Benchmark-ready**: can be extended for throughput tests.

---

### Variants

- Threaded server (`server.py`): simple thread-per-connection model.
- Async server (`server_async.py`): event-loop concurrency with asyncio (fewer threads, scalable for I/O-bound workloads).
- C++ server/client (`cpp/server.cpp`, `cpp/client.cpp`): minimal POSIX sockets implementation (low-level systems).

---

## How to Run

1. Start the server:

   ```bash
   python3 server.py --host 0.0.0.0 --port 5050
   ```

   You should see:

   ```bash
   [server] listening on 0.0.0.0:5050
   ```

2. In another terminal, run the client:

   ```bash
   python3 client.py --host 127.0.0.1 --port 5050 --message 'Hello Annapurna!'
   ```

   Example output:

   ```bash
   [client] sent    : b'Hello Annapurna!'
   [client] received: b'Hello Annapurna!'
   [client] RTT     : 2.119 ms
   ```

---

## Asyncio Variant

Run the event-loop server:

```bash
python3 server_async.py --host 0.0.0.0 --port 5051
```

Client example:

```bash
python3 client.py --host 127.0.0.1 --port 5051 --message 'hello-async'
```

---

## C++ Variant (POSIX sockets)

This pair demonstrates a low-level echo implementation using POSIX sockets in C++.

### Build (macOS/Linux)

from project root

```bash
mkdir -p cpp/build
c++ -std=c++17 -O2 -Wall -Wextra -pedantic -o cpp/build/server cpp/server.cpp
c++ -std=c++17 -O2 -Wall -Wextra -pedantic -o cpp/build/client cpp/client.cpp
```

### Run

Terminal A

```bash
./cpp/build/server 5052
```

Terminal B

```bash
./cpp/build/client 127.0.0.1 5052 "Hello from C++!"
```

---

## Performance Notes

- **Environment:** macOS (Apple M2, Python 3.11).  
- **Latency:** ~1–3 ms RTT on loopback (localhost).  
- **Throughput:** Sustained ~150–200 MB/s with larger payloads in tight loops.  
- **Async server (localhost, 16 KB msg × 1000):** avg RTT ≈ 0.089 ms, p95 ≈ 0.122 ms, throughput ≈ 172.61 MB/s.
- **Single-message RTT example (async server):** ≈ 5.5 ms (varies with background load and scheduling).
- **C++ client single-message RTT (localhost):** ≈ 0.03 ms (varies by machine; measured on macOS/M2).

---

## Project Layout

```text
.
├── client.py  
├── server.py  
├── server_async.py  
├── cpp/  
│   ├── client.cpp  
│   └── server.cpp  
├── README.md  
└── benchmarks.md
```

---

## Future Improvements

- Add asyncio-based server for higher concurrency.
- Add SSL/TLS support for secure echo.
- Automate benchmarking (latency + throughput graphs).
