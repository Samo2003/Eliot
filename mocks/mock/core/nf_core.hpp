#ifndef NF_CORE_H
#define NF_CORE_H

#include <arpa/inet.h>
#include <fcntl.h>
#include <netinet/in.h>
#include <optional>
#include <queue>
#include <array>

#include "../config/config.hpp"
#include "socket.hpp"
#include "nf_packet.hpp"

namespace nf_queue_mock {

/**
 * @brief Core engine for mock NFQueue backend.
 */
class NFCore {
public:
    /**
     * @brief Construct NFCore using configuration.
     */
    explicit NFCore(const Config& config) 
        : _receive_socket(_make_recv_socket(config.eliot_ip, config.eliot_port)),
        _send_socket(_make_send_socket()) {
            _translate_address(config.client_ip, config.client_port, _client_addr);
            _translate_address(config.server_ip, config.server_port, _server_addr);  
        }

    /**
     * @brief Receive packets and enqueue them.
     */
    void accept_packets(void) noexcept;

    /**
     * @brief Send data to configured client endpoint.
     *
     * @return true if full payload was transmitted.
     */
    inline bool send_to_client(const std::vector<uint8_t>& data) const noexcept {
        ssize_t n = sendto(
            _send_socket.get(),
            data.data(),
            data.size(), 
            0,
            reinterpret_cast<const sockaddr*>(&_client_addr),
            sizeof(_client_addr)
        );
        return n == data.size();
    }

    /**
     * @brief Send data to configured server endpoint.
     *
     * @return true if full payload was transmitted.
     */
    inline bool send_to_server(const std::vector<uint8_t>& data) const noexcept {
        ssize_t n = sendto(
            _send_socket.get(),
            data.data(),
            data.size(),
            0,
            reinterpret_cast<const sockaddr*>(&_server_addr),
            sizeof(_server_addr)
        );
        return n == data.size();
    }
    
    /**
     * @brief Pop next packet from internal queue.
     */
    std::optional<NFQueuePacket> queue_pop(void) noexcept;

private:
    ///> Socket used for receiving packets
    Socket _receive_socket;

    ///> Socket used for outgoing transmissions
    Socket _send_socket;

    ///> Pre-translated client address
    sockaddr_in _client_addr{};

    ///> Pre-translated server address
    sockaddr_in _server_addr{};

    ///> FIFO packet buffer
    std::queue<NFQueuePacket> _queue;

    ///> Create and configure receive socket
    static Socket _make_recv_socket(const std::string& bind_addr, uint16_t port);

    ///> Create send socket
    static Socket _make_send_socket(void);

    ///> Translate textual IP + port to sockaddr_in
    static void _translate_address(const std::string& ip, uint16_t port, sockaddr_in& addr);
};

}   // namespace nf_queue_mock

#endif
