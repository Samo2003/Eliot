#ifndef NF_CORE_H
#define NF_CORE_H

#include <arpa/inet.h>
#include <fcntl.h>
#include <netinet/in.h>
#include <optional>
#include <queue>
#include <iostream>

#include "socket.hpp"
#include "nf_packet.hpp"

namespace nf_queue_echo {

class NFCore {
public:
    explicit NFCore() 
        : _socket(_make_socket(_ip, _port)) {}

    void accept_packets(void) noexcept;

    const bool send(const NFQueuePacket&& packet) const noexcept;
    
    std::optional<NFQueuePacket> queue_pop(void) noexcept;

private:
    Socket _socket;
    std::queue<NFQueuePacket> _queue;
    static constexpr const char* _ip = "127.0.0.1";
    static constexpr int _port = 0;

    static Socket _make_socket(const char* bind_addr, uint16_t port);
};

}   // namespace nf_queue_echo

#endif
