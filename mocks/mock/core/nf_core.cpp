#include "nf_core.hpp"

namespace nf_queue_mock {

/**
 * @brief Create non-blocking UDP socket for receiving packets.
 */
Socket NFCore::_make_recv_socket(const std::string& bind_addr, uint16_t port) {
    int fd = ::socket(AF_INET, SOCK_DGRAM, 0);
    if (fd < 0) {
        throw std::runtime_error("Failed to create receive socket");
    }

    int bufsize = 4 * 1024 * 1024;
    int one = 1;

    // Configure reuse + receive buffer
    if (setsockopt(fd, SOL_SOCKET, SO_REUSEADDR, &one, sizeof(one)) < 0 ||
        setsockopt(fd, SOL_SOCKET, SO_RCVBUF, &bufsize, sizeof(bufsize)) < 0) {
        ::close(fd);
        throw std::runtime_error("Failed to set SO_REUSEADDR");
    }

    // Enable non-blocking mode
    int flags = fcntl(fd, F_GETFL, 0);
    if (flags < 0 || fcntl(fd, F_SETFL, flags | O_NONBLOCK) < 0) { 
        ::close(fd); 
        throw std::runtime_error("Failed to set socket flags"); 
    }

    sockaddr_in sa{};
    sa.sin_family = AF_INET;
    sa.sin_port = htons(port);
    if (inet_pton(AF_INET, bind_addr.c_str(), &sa.sin_addr) != 1) {
        ::close(fd);
        throw std::runtime_error("invalid bind address");
    }
    if (::bind(fd, reinterpret_cast<sockaddr*>(&sa), sizeof(sa)) < 0) {
        ::close(fd);
        throw std::runtime_error("Failed to bind address");
    }

    return Socket(fd);
}

/**
 * @brief Create UDP socket used for outgoing packets.
 */
Socket NFCore::_make_send_socket() {
    int fd = ::socket(AF_INET, SOCK_DGRAM, 0);
    if (fd < 0) {
        throw std::runtime_error("Failed to create send socket");
    }
    int bufsize = 4 * 1024 * 1024;
    if (setsockopt(fd, SOL_SOCKET, SO_SNDBUF, &bufsize, sizeof(bufsize)) < 0) {
        ::close(fd);
        throw std::runtime_error("Failed to set SO_SNDBUF");
    }
    return Socket(fd);
}

/**
 * @brief Translate textual IP + port into sockaddr_in structure.
 */
void NFCore::_translate_address(const std::string& ip, uint16_t port, sockaddr_in& addr) {
    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);
    if (inet_pton(AF_INET, ip.c_str(), &addr.sin_addr) != 1)
        throw std::runtime_error("Invalid IP address");
}

/**
 * @brief Pop next packet from internal queue.
 */
std::optional<NFQueuePacket> NFCore::queue_pop() noexcept {
    if (_queue.empty())
        return std::nullopt; 
    NFQueuePacket packet = std::move(_queue.front());
    _queue.pop();
    return std::move(packet);
}

/**
 * @brief Receive all available packets from non-blocking socket.
 *
 * Packets origin is classified based on source address.
 */
void NFCore::accept_packets() noexcept {
    std::array<uint8_t, UINT16_MAX + 1> buf;
    while (true) {
        sockaddr_in from{};
        socklen_t fromlen = sizeof(from);
        ssize_t n = recvfrom(
            _receive_socket.get(),
            buf.data(),
            buf.size(),
            0,
            reinterpret_cast<sockaddr*>(&from),
            &fromlen
        );
        if (n < 0) {
            if (errno != EAGAIN && errno != EWOULDBLOCK) 
                perror("recvfrom");
            break;
        }
        std::vector<uint8_t> payload(buf.begin(), buf.begin() + n);
        NFQueuePacket::Origin origin = NFQueuePacket::Origin::Unknown;
        if (from.sin_addr.s_addr == _client_addr.sin_addr.s_addr && from.sin_port == _client_addr.sin_port) 
            origin = NFQueuePacket::Origin::Client;
        else if (from.sin_addr.s_addr == _server_addr.sin_addr.s_addr && from.sin_port == _server_addr.sin_port) 
            origin = NFQueuePacket::Origin::Server;
        _queue.push(NFQueuePacket(std::move(payload), origin));
    }
}

}   // namespace nf_queue_mock
