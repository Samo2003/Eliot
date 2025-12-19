#ifndef NF_QUEUE_SOCKET_H
#define NF_QUEUE_SOCKET_H

#include <unistd.h>
#include <utility>

namespace nf_queue_echo {
    class Socket {
        public:
            explicit Socket(int fd = -1) noexcept : _fd(fd) {}
            ~Socket() noexcept { if (_fd >= 0) ::close(_fd); }

            Socket(const Socket&) = delete;
            Socket& operator=(const Socket&) = delete;

            Socket(Socket&& other) noexcept : _fd(std::exchange(other._fd, -1)) {}
            Socket& operator=(Socket&& other) noexcept {
                if (this != &other) {
                    if (_fd >= 0)
                        ::close(_fd);
                    _fd = std::exchange(other._fd, -1);
                }
                return *this;
            }

            const int get() const noexcept { return _fd; }
            explicit operator bool() const noexcept { return _fd >= 0; }
        private:
            int _fd;
    };
}

#endif
