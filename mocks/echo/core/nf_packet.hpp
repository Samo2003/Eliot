#ifndef NF_PACKET_H
#define NF_PACKET_H

#include <vector>
#include <netinet/in.h>

namespace nf_queue_echo {

/**
 * @brief Represents a received packet within NFQueue backend.
 *
 * This is a move-only type to avoid unnecessary payload copies.
 */
class NFQueuePacket {
public:
    /**
     * @brief Construct packet from payload and source address.
     *
     * @param payload Raw packet data (moved into object)
     * @param from    Source IPv4 address structure
     */
    explicit NFQueuePacket(std::vector<uint8_t>&& payload, struct sockaddr_in from) noexcept
        : _payload(std::move(payload)),
            _from(from) {}

    // Move semantics
    NFQueuePacket(NFQueuePacket&&) noexcept = default;
    NFQueuePacket& operator=(NFQueuePacket&&) noexcept = default;

    // Disable copying
    NFQueuePacket(const NFQueuePacket&) = delete;
    NFQueuePacket& operator=(const NFQueuePacket&) = delete;

    /**
     * @brief Access packet payload.
     *
     * @return Const reference to internal byte buffer.
     */
    inline const std::vector<uint8_t>& get_payload() const noexcept { return _payload; }

    /**
     * @brief Access sender address.
     *
     * @return Pointer to sockaddr_in structure.
     */
    inline const struct sockaddr_in* get_from() const noexcept { return &_from; }

private:
    ///< Raw packet data
    std::vector<uint8_t> _payload;
    ///< Sender IPv4 address
    struct sockaddr_in _from;
};

}   // namespace nf_queue_echo

#endif
