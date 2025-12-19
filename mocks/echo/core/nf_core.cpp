#include "nf_core.hpp"

namespace nf_queue_echo {
    Socket NFCore::_make_socket(const char* bind_addr, uint16_t port) {
        int fd = ::socket(AF_INET, SOCK_DGRAM, 0);
        if (fd < 0) {
            throw std::runtime_error("Failed to create receive socket");
        }

        int bufsize = 4 * 1024 * 1024;
        int one = 1;
        if (setsockopt(fd, SOL_SOCKET, SO_REUSEADDR, &one, sizeof(one)) < 0 ||
            setsockopt(fd, SOL_SOCKET, SO_RCVBUF, &bufsize, sizeof(bufsize)) < 0 ||
            setsockopt(fd, SOL_SOCKET, SO_SNDBUF, &bufsize, sizeof(bufsize)) < 0) {
            ::close(fd);
            throw std::runtime_error("Failed to set SO_REUSEADDR");
        }

        int flags = fcntl(fd, F_GETFL, 0);
        if (flags < 0 || fcntl(fd, F_SETFL, flags | O_NONBLOCK) < 0) { 
            ::close(fd); 
            throw std::runtime_error("Failed to set socket flags"); 
        }

        sockaddr_in sa{};
        sa.sin_family = AF_INET;
        sa.sin_port = htons(port);
        if (inet_pton(AF_INET, bind_addr, &sa.sin_addr) != 1) {
            ::close(fd);
            throw std::runtime_error("invalid bind address");
        }
        if (::bind(fd, reinterpret_cast<sockaddr*>(&sa), sizeof(sa)) < 0) {
            ::close(fd);
            throw std::runtime_error("Failed to bind address");
        }

        socklen_t len = sizeof(sa);
        if (::getsockname(fd, reinterpret_cast<sockaddr*>(&sa), &len) < 0) {
            ::close(fd);
            throw std::runtime_error("getsockname failed");
        }

        uint16_t given_port = ntohs(sa.sin_port);
        std::cout << "LISTEN_PORT=" << given_port << std::endl;
        std::cout.flush();

        return Socket(fd);
    }

    const bool NFCore::send(const NFQueuePacket&& packet) const noexcept {
        const std::vector<uint8_t>& payload = packet.get_payload();
        const struct sockaddr_in* from = packet.get_from();
        ssize_t n = sendto(_socket.get(), payload.data(), payload.size(), 0, reinterpret_cast<const sockaddr*>(from), sizeof(struct sockaddr_in));
        return n == payload.size();
    }

    std::optional<NFQueuePacket> NFCore::queue_pop() noexcept {
        if (_queue.empty())
            return std::nullopt; 
        NFQueuePacket packet = std::move(_queue.front());
        _queue.pop();
        return std::move(packet);
    }

    void NFCore::accept_packets() noexcept {
        while (true) {
            uint8_t buf[UINT16_MAX + 1];
            sockaddr_in from{};
            socklen_t fromlen = sizeof(from);
            ssize_t n = recvfrom(_socket.get(), buf, sizeof(buf), 0, reinterpret_cast<sockaddr*>(&from), &fromlen);
            if (n < 0) {
                if (errno != EAGAIN && errno != EWOULDBLOCK) 
                    perror("recvfrom");
                break;
            }
            std::vector<uint8_t> payload(buf, buf + n);
            _queue.push(NFQueuePacket(_packet_id++, std::move(payload), from));
        }
    }

}
