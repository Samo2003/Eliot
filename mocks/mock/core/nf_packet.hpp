#ifndef NF_PACKET_H
#define NF_PACKET_H

#include <vector>

namespace nf_queue_mock {

/**
 * @brief Packet abstraction for mock backend.
 *
 * Represents a packet together with its logical origin.
 */
class NFQueuePacket {
public:
    /**
     * @brief Logical origin of packet.
     */
    enum class Origin { Unknown = 0, Server, Client };

    /**
     * @brief Construct packet with payload and origin.
     *
     * @param payload Raw packet data (moved into object)
     * @param origin  Packet origin classification
     */
    explicit NFQueuePacket(std::vector<uint8_t>&& payload, Origin origin) noexcept
        : _payload(std::move(payload)),
            _origin(origin) {}

    // Move-only semantics
    NFQueuePacket(NFQueuePacket&&) noexcept = default;
    NFQueuePacket& operator=(NFQueuePacket&&) noexcept = default;

    // Disable copying
    NFQueuePacket(const NFQueuePacket&) = delete;
    NFQueuePacket& operator=(const NFQueuePacket&) = delete;

    /**
     * @brief Access packet payload.
     */
    inline const std::vector<uint8_t>& get_payload() const noexcept {
        return _payload;
    }

    /**
     * @brief Get packet origin.
     */
    inline Origin get_origin() const noexcept {
        return _origin; 
    }

private:
    ///> Raw packet data
    std::vector<uint8_t> _payload;

    ///> Packet origin
    Origin _origin = Origin::Unknown;
};

}   // namespace nf_queue_mock

#endif
