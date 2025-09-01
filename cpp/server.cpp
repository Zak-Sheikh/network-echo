// server.cpp - Minimal POSIX TCP Echo Server
// ------------------------------------------
// Listens on a given port, accepts one client at a time,
// and echoes back any bytes received until the client closes.

#include <arpa/inet.h>
#include <netdb.h>
#include <sys/socket.h>
#include <unistd.h>

#include <cerrno>
#include <cstring>
#include <iostream>

static void die(const char* msg) {
    std::cerr << msg << ": " << std::strerror(errno) << "\n";
    std::exit(1);
}

int main(int argc, char** argv) {
    const char* host = "0.0.0.0";
    const char* port = "5052";           // default C++ port
    if (argc >= 2) port = argv[1];       // usage: ./server <port>

    addrinfo hints{};
    hints.ai_family   = AF_INET;         // IPv4
    hints.ai_socktype = SOCK_STREAM;     // TCP
    hints.ai_flags    = AI_PASSIVE;      // for bind

    addrinfo* res;
    if (getaddrinfo(host, port, &hints, &res) != 0) die("getaddrinfo");

    int listen_fd = socket(res->ai_family, res->ai_socktype, res->ai_protocol);
    if (listen_fd < 0) die("socket");

    int yes = 1;
    if (setsockopt(listen_fd, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(yes)) < 0)
        die("setsockopt");

    if (bind(listen_fd, res->ai_addr, res->ai_addrlen) < 0) die("bind");
    freeaddrinfo(res);

    if (listen(listen_fd, SOMAXCONN) < 0) die("listen");

    std::cout << "[cpp-server] listening on " << host << ":" << port << "\n";

    constexpr size_t BUFSZ = 4096;
    char buf[BUFSZ];

    while (true) {
        sockaddr_in cli{};
        socklen_t clilen = sizeof(cli);
        int conn = accept(listen_fd, (sockaddr*)&cli, &clilen);
        if (conn < 0) {
            if (errno == EINTR) continue;
            die("accept");
        }

        while (true) {
            ssize_t n = recv(conn, buf, BUFSZ, 0);
            if (n < 0) { close(conn); die("recv"); }
            if (n == 0) break;           // client closed
            ssize_t sent = 0;
            while (sent < n) {
                ssize_t m = send(conn, buf + sent, n - sent, 0);
                if (m <= 0) { close(conn); die("send"); }
                sent += m;
            }
        }
        close(conn);
    }
}
