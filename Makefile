# Simple build/run helpers

PYTHON ?= python3
CXX ?= c++
CXXFLAGS ?= -std=c++17 -O2 -Wall -Wextra -pedantic

all: build-cpp

# ---- Python helpers ----
run-server:
	$(PYTHON) server.py --host 0.0.0.0 --port 5050

run-server-async:
	$(PYTHON) server_async.py --host 0.0.0.0 --port 5051

run-client:
	$(PYTHON) client.py --host 127.0.0.1 --port 5050 --message "ping"

bench-1k:
	$(PYTHON) client.py --host 127.0.0.1 --port 5050 --message "$$(python3 -c "print('x'*1024)")" --bench --repeat 2000

# ---- C++ build/run ----
build-cpp: cpp/build/server cpp/build/client

cpp/build/server: cpp/server.cpp
	mkdir -p cpp/build
	$(CXX) $(CXXFLAGS) -o $@ $<

cpp/build/client: cpp/client.cpp
	mkdir -p cpp/build
	$(CXX) $(CXXFLAGS) -o $@ $<

run-cpp-server:
	./cpp/build/server 5052

run-cpp-client:
	./cpp/build/client 127.0.0.1 5052 "Hello from Makefile"

clean:
	rm -rf cpp/build

