#ifndef NF_PACKET_H
#define NF_PACKET_H

#include <vector>
#include <memory>

namespace nf_queue_benchmark {

/**
 * @brief Packet wrapper used in benchmarking backend.
 *
 * This implementation does NOT own payload memory.
 * It stores a reference to externally managed buffer.
 */
class NFQueuePacket {
public:
    /**
     * @brief Construct packet wrapper from external payload reference.
     *
     * @param p Reference to payload buffer
     */
    explicit NFQueuePacket(std::vector<uint8_t>& p) noexcept : _payload(p) {}
    
    // Move constructor allowed
    NFQueuePacket(NFQueuePacket&&) noexcept = default;

    // Move assignment deleted
    NFQueuePacket& operator=(NFQueuePacket&&) noexcept = delete;

    // Copy disabled
    NFQueuePacket(const NFQueuePacket&) = delete;
    NFQueuePacket& operator=(const NFQueuePacket&) = delete;
    
    /**
     * @brief Access payload buffer.
     */
    inline std::vector<uint8_t>& get_payload() const noexcept { return _payload; }

private:
    ///> Non-owning reference
    std::vector<uint8_t>& _payload;
};

}   // namespace nf_queue_benchmark

#endif
