#ifndef NF_QUEUE_PROFILING_H
#define NF_QUEUE_PROFILING_H

#include <optional>
#include <cstdint>
#include "nf_packet.hpp"
#include <iostream>

namespace nf_queue_profiling {
    class NFQueue {
        public: 
            NFQueue() {
                _packets.reserve(_PACKET_COUNT);

                for (size_t i = 0; i < _PACKET_COUNT; i++) {
                    _packets.emplace_back(NFQueuePacket(_template_payload));
                }
            }

            inline NFQueuePacket* get_packet() noexcept {
                return _index < _PACKET_COUNT ? &_packets[_index++] : nullptr;
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
            std::vector<NFQueuePacket> _packets;
            std::vector<uint8_t> _template_payload{_PAYLOAD_SIZE, 0xAB};
            size_t _index = 0;
    };
}

#endif
