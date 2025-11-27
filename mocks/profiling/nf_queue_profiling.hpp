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

                auto template_payload = std::make_shared<std::vector<uint8_t>>(_PAYLOAD_SIZE, 0xAB);

                for (size_t i = 0; i < _PACKET_COUNT; i++) {
                    _packets.emplace_back(NFQueuePacket(template_payload));
                }
            }

            inline NFQueuePacket* get_packet() noexcept {
                if (_index < _PACKET_COUNT)
                    return &_packets[_index++];
                return nullptr;
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
            size_t _index = 0;
    };
}

#endif
