#ifndef NF_PACKET_H
#define NF_PACKET_H

#include <vector>

namespace nf_queue_profiling {
    class NFQueuePacket {
        private:
            std::vector<uint8_t> _payload;

        public:
            explicit NFQueuePacket(std::vector<uint8_t>&& payload) noexcept
                : _payload(std::move(payload)) {}

            
            NFQueuePacket(NFQueuePacket&&) noexcept = default;
            NFQueuePacket& operator=(NFQueuePacket&&) noexcept = default;
            NFQueuePacket(const NFQueuePacket&) = delete;
            NFQueuePacket& operator=(const NFQueuePacket&) = delete;

            inline constexpr const std::vector<uint8_t>& get_payload() const noexcept { return _payload; }
    };
}

#endif
