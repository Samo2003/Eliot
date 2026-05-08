#ifndef NF_CORE_H
#define NF_CORE_H

#include <arpa/inet.h>
#include <fcntl.h>
#include <netinet/in.h>
#include <optional>
#include <queue>
#include <iostream>
#include <cerrno>
#include <cstdint>
#include <array>

#include "socket.hpp"
#include "nf_packet.hpp"

namespace nf_queue_echo {

/**
 * @brief Core packet processing backend for echo NFQueue mode.
 *
 * NFCore encapsulates low-level socket communication and
 * packet buffering logic.
 */
class NFCore {
public:
    /**
     * @brief Construct NFCore and bind socket.
     *
     * Automatically creates and binds socket
     * to configured IP and port.
     */
    explicit NFCore() 
        : _socket(_make_socket(_ip, _port)) {}

    /**
     * @brief Receive packets from socket and enqueue them.
     */
    void accept_packets(void) noexcept;

    /**
     * @brief Send packet through backend socket.
     *
     * @param packet Packet to send (rvalue)
     * @return true if sending succeeded
     */
    bool send(NFQueuePacket&& packet) const noexcept;
    
    /**
     * @brief Pop next packet from internal queue.
     *
     * @return Optional packet if queue not empty.
     */
    std::optional<NFQueuePacket> queue_pop(void) noexcept;

private:
    ///> RAII UDP socket
    Socket _socket;

    ///> FIFO buffer storing received packets
    std::queue<NFQueuePacket> _queue;

    ///> Default bind address
    static constexpr const char* _ip = "127.0.0.1";

    /// Port 0 = let OS assign port
    static constexpr int _port = 0;

    /**
     * @brief Create and bind socket.
     *
     * @param bind_addr Address to bind
     * @param port Port to bind
     */
    static Socket _make_socket(const char* bind_addr, uint16_t port);
};

}   // namespace nf_queue_echo

#endif
