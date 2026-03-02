#ifndef NF_QUEUE_PROFILING_H
#define NF_QUEUE_PROFILING_H

#include <optional>
#include <cstdint>
#include "nf_packet.hpp"
#include <iostream>

namespace nf_queue_profiling {

/**
 * @brief Synthetic profiling backend.
 */
class NFQueue {
public: 
    /**
     * @brief Construct profiling backend.
     */
    NFQueue() 
        : _template_payload{_PAYLOAD_SIZE, 0xAB},
            _packet(_template_payload)
    {}

    /**
     * @brief Return next synthetic packet.
     *
     * Returns nullptr when limit reached.
     */
    inline NFQueuePacket* get_packet() noexcept {
        if (_index >= _PACKET_COUNT) return nullptr;
        ++_index;
        return &_packet;
    }

    /**
     * @brief Accept packet (no-op in profiling mode).
     */
    inline void accept_packet(NFQueuePacket&& packet) const noexcept {}

    /**
     * @brief Drop packet (no-op in profiling mode).
     */
    inline void drop_packet(NFQueuePacket&& packet) const noexcept {}

    /**
     * @brief Print profiling statistics on destruction
     */
    ~NFQueue() {
        std::cerr << "Processed:" << _index << std::endl;
        std::cerr << "Total:" << _PACKET_COUNT << std::endl;
    }

private:
    ///> Total number of synthetic packets to generate
    static constexpr size_t _PACKET_COUNT = 100000000;

    ///> Payload size for synthetic packet
    static constexpr size_t _PAYLOAD_SIZE = 128;

    ///> Shared payload buffer reused across all packets
    std::vector<uint8_t> _template_payload;

    ///> Single reusable packet wrapper
    NFQueuePacket _packet;

    ///> Current processed packet count
    size_t _index = 0;
};

}   // namespace nf_queue_profiling

#endif
