#ifndef NF_PACKET_H
#define NF_PACKET_H

#include <vector>
#include <netinet/in.h>

namespace nf_queue_echo {
    class NFQueuePacket {
        private:
            uint64_t _id;
            std::vector<uint8_t> _payload;
            struct sockaddr_in _from;

        public:
            explicit NFQueuePacket(uint64_t i, std::vector<uint8_t>&& payload, struct sockaddr_in from) noexcept
                : _id(i),
                _payload(std::move(payload)),
                _from(from) {}

            
            NFQueuePacket(NFQueuePacket&&) noexcept = default;
            NFQueuePacket& operator=(NFQueuePacket&&) noexcept = default;
            NFQueuePacket(const NFQueuePacket&) = delete;
            NFQueuePacket& operator=(const NFQueuePacket&) = delete;

            inline constexpr const uint64_t get_id() const noexcept { return _id; }
            inline constexpr const std::vector<uint8_t>& get_payload() const noexcept { return _payload; }
            inline constexpr const struct sockaddr_in* get_from() const noexcept { return &_from; }
    };
}

#endif
