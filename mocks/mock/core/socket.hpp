#ifndef NF_QUEUE_SOCKET_H
#define NF_QUEUE_SOCKET_H

#include <unistd.h>
#include <utility>

namespace nf_queue_mock {

/**
 * @brief RAII wrapper for POSIX socket file descriptor.
 *
 * Ensures no file descriptor leaks occur.
 */
class Socket {
public:
    /**
     * @brief Construct socket wrapper.
     *
     * @param fd File descriptor (default = invalid)
     */
    explicit Socket(int fd = -1) noexcept : _fd(fd) {}

    /**
     * @brief Destructor closes descriptor if valid.
     */
    ~Socket() noexcept { if (_fd >= 0) ::close(_fd); }

    // Non-copyable
    Socket(const Socket&) = delete;
    Socket& operator=(const Socket&) = delete;

    /**
     * @brief Move constructor.
     */
    Socket(Socket&& other) noexcept 
        : _fd(std::exchange(other._fd, -1)) {}

    /**
     * @brief Move assignment.
     */
    Socket& operator=(Socket&& other) noexcept {
        if (this != &other) {
            if (_fd >= 0)
                ::close(_fd);
            _fd = std::exchange(other._fd, -1);
        }
        return *this;
    }

    /**
     * @brief Get underlying file descriptor.
     */
    int get() const noexcept { return _fd; }

    /**
     * @brief Check if descriptor is valid.
     */
    explicit operator bool() const noexcept { return _fd >= 0; }

private:
    ///> POSIX file descriptor
    int _fd;
};

}   // namespace nf_queue_mock

#endif
