/// client.cpp - Minimal POSIX TCP Echo Client
// ------------------------------------------
// Connects to the echo server, sends a message, waits for the echo,
// and prints the round-trip time (RTT).

#include <arpa/inet.h>
#include <netdb.h>
#include <sys/socket.h>
#include <unistd.h>

#include <chrono>
#include <cstring>
#include <iostream>
#include <string>
#include <vector>
#include <signal.h>


static void die(const char* msg) {
    std::cerr << msg << ": " << std::strerror(errno) << "\n";
    std::exit(1);
}

int main(int argc, char** argv) {
    signal(SIGPIPE, SIG_IGN);
    const char* host = "127.0.0.1";
    const char* port = "5052";
    std::string msg = "Hello from C++!";

    // usage: ./client <host> <port> [message]
    if (argc >= 2) host = argv[1];
    if (argc >= 3) port = argv[2];
    if (argc >= 4) msg  = argv[3];

    addrinfo hints{};
    hints.ai_family   = AF_INET;
    hints.ai_socktype = SOCK_STREAM;

    addrinfo* res;
    if (getaddrinfo(host, port, &hints, &res) != 0) die("getaddrinfo");

    int fd = socket(res->ai_family, res->ai_socktype, res->ai_protocol);
    if (fd < 0) die("socket");

    if (connect(fd, res->ai_addr, res->ai_addrlen) < 0) die("connect");
    freeaddrinfo(res);

    auto t0 = std::chrono::high_resolution_clock::now();

    // send exact
    size_t remaining = msg.size();
    const char* p = msg.data();
    while (remaining > 0) {
        ssize_t n = send(fd, p, remaining, 0);
        if (n <= 0) { close(fd); die("send"); }
        p += n;
        remaining -= n;
    }

    // recv exact
    std::vector<char> buf(msg.size());
    size_t got = 0;
    while (got < msg.size()) {
        ssize_t n = recv(fd, buf.data() + got, msg.size() - got, 0);
        if (n <= 0) { close(fd); die("recv"); }
        got += n;
    }

    auto t1 = std::chrono::high_resolution_clock::now();
    close(fd);

    std::string echoed(buf.begin(), buf.end());
    if (echoed != msg) {
        std::cerr << "mismatch: '" << echoed << "' vs '" << msg << "'\n";
        return 2;
    }

    auto us = std::chrono::duration_cast<std::chrono::microseconds>(t1 - t0).count();
    std::cout << "[cpp-client] sent : \"" << msg << "\"\n";
    std::cout << "[cpp-client] RTT  : " << us / 1000.0 << " ms\n";
}
