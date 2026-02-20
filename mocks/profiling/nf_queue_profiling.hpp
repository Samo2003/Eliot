#ifndef NF_QUEUE_PROFILING_H
#define NF_QUEUE_PROFILING_H

#include <optional>
#include <cstdint>
#include "nf_packet.hpp"
#include <iostream>

namespace nf_queue_profiling {

class NFQueue {
public: 
    NFQueue() 
        : _template_payload{_PAYLOAD_SIZE, 0xAB},
            _packet(_template_payload)
    {}

    inline NFQueuePacket* get_packet() noexcept {
        if (_index >= _PACKET_COUNT) return nullptr;
        ++_index;
        return &_packet;
    }

    inline void accept_packet(NFQueuePacket&& packet) const noexcept {}

    inline void drop_packet(NFQueuePacket&& packet) const noexcept {}

    ~NFQueue() {
        std::cerr << "Processed:" << _index << std::endl;
        std::cerr << "Total:" << _PACKET_COUNT << std::endl;
    }

private:
    static constexpr size_t _PACKET_COUNT = 100000000;
    static constexpr size_t _PAYLOAD_SIZE = 128;

    std::vector<uint8_t> _template_payload;
    NFQueuePacket _packet;
    size_t _index = 0;
};

}   // namespace nf_queue_profiling

#endif
