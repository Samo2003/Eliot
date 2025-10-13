#ifndef NF_PACKET_H
#define NF_PACKET_H

#include <vector>

namespace nf_queue {
    enum class Origin { Unknown = 0, Server, Client };

    class NFQueuePacket {
        private:
            uint64_t _id;
            std::vector<uint8_t> _payload;
            Origin _origin = Origin::Unknown;

        public:
            explicit NFQueuePacket(uint64_t i, std::vector<uint8_t>&& payload, Origin origin) noexcept
                : _id(i),
                _payload(std::move(payload)),
                _origin(origin) {}

            
            NFQueuePacket(NFQueuePacket&&) noexcept = default;
            NFQueuePacket& operator=(NFQueuePacket&&) noexcept = default;
            NFQueuePacket(const NFQueuePacket&) = delete;
            NFQueuePacket& operator=(const NFQueuePacket&) = delete;

            inline const uint64_t get_id() const noexcept { return _id; }
            inline const std::vector<uint8_t>& get_payload() const noexcept { return _payload; }
            inline const Origin get_origin() const noexcept { return _origin; }
    };
}

#endif
