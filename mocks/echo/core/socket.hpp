#ifndef NF_QUEUE_SOCKET_H
#define NF_QUEUE_SOCKET_H

#include <unistd.h>
#include <utility>

namespace nf_queue_echo {

/**
 * @brief RAII wrapper for POSIX socket file descriptor.
 *
 * Ensures that file descriptor is properly closed
 * when object goes out of scope.
 */
class Socket {
public:
    /**
     * @brief Construct Socket with given file descriptor.
     *
     * @param fd File descriptor (default = invalid)
     */
    explicit Socket(int fd = -1) noexcept : _fd(fd) {}

    /**
     * @brief Destructor closes file descriptor if valid.
     */
    ~Socket() noexcept { if (_fd >= 0) ::close(_fd); }

    // Non-copyable (unique ownership)
    Socket(const Socket&) = delete;
    Socket& operator=(const Socket&) = delete;

    /**
     * @brief Move constructor.
     *
     * Transfers ownership of file descriptor.
     */
    Socket(Socket&& other) noexcept : _fd(std::exchange(other._fd, -1)) {}

    /**
     * @brief Move assignment operator.
     *
     * Releases current descriptor and takes ownership
     * from other instance.
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
     * @brief Check whether socket is valid.
     */
    explicit operator bool() const noexcept { 
        return _fd >= 0;
    }

private:
    ///< POSIX file descriptor
    int _fd;
};

}   // namespace nf_queue_echo

#endif
