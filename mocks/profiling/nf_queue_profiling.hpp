#ifndef NF_QUEUE_PROFILING_H
#define NF_QUEUE_PROFILING_H

#include <optional>
#include <cstdint>
#include "nf_packet.hpp"

namespace nf_queue_profiling {
    class NFQueue {
        public: 
            NFQueue() {
                _packets.reserve(_PACKET_COUNT);
                std::vector<uint8_t> template_payload(_PAYLOAD_SIZE, 0xAB);

                for (size_t i = 0; i < _PACKET_COUNT; i++)
                    _packets.emplace_back(std::vector<uint8_t>(template_payload));
            }

            inline std::optional<NFQueuePacket> get_packet() noexcept {
                if (_index < _PACKET_COUNT)
                    return std::move(_packets[_index++]);
                return std::nullopt;
            }

            inline void accept_packet(NFQueuePacket&& packet) const noexcept {}

            inline void drop_packet(NFQueuePacket&& packet) const noexcept {}

        private:
            static constexpr ssize_t _PACKET_COUNT = 1000000;
            static constexpr ssize_t _PAYLOAD_SIZE = 128;
            std::vector<NFQueuePacket> _packets;
            size_t _index = 0;
    };
}

#endif
