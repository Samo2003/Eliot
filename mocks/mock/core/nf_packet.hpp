#ifndef NF_PACKET_H
#define NF_PACKET_H

#include <vector>

namespace nf_queue_mock {

    
class NFQueuePacket {
public:
    enum class Origin { Unknown = 0, Server, Client };
    explicit NFQueuePacket(std::vector<uint8_t>&& payload, Origin origin) noexcept
        : _payload(std::move(payload)),
            _origin(origin) {}

    
    NFQueuePacket(NFQueuePacket&&) noexcept = default;
    NFQueuePacket& operator=(NFQueuePacket&&) noexcept = default;
    NFQueuePacket(const NFQueuePacket&) = delete;
    NFQueuePacket& operator=(const NFQueuePacket&) = delete;

    inline constexpr const std::vector<uint8_t>& get_payload() const noexcept { return _payload; }
    inline constexpr const Origin get_origin() const noexcept { return _origin; }

private:
    std::vector<uint8_t> _payload;
    Origin _origin = Origin::Unknown;
};

}   // namespace nf_queue_mock

#endif
