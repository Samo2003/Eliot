#ifndef NF_PACKET_H
#define NF_PACKET_H

#include <vector>
#include <memory>

namespace nf_queue_profiling {

class NFQueuePacket {
public:
    explicit NFQueuePacket(std::vector<uint8_t>& p) noexcept : _payload(p) {}
    
    
    NFQueuePacket(NFQueuePacket&&) noexcept = default;
    NFQueuePacket& operator=(NFQueuePacket&&) noexcept = delete;
    NFQueuePacket(const NFQueuePacket&) = delete;
    NFQueuePacket& operator=(const NFQueuePacket&) = delete;
    
    inline std::vector<uint8_t>& get_payload() const noexcept { return _payload; }

private:
    std::vector<uint8_t>& _payload;
};

}   // namespace nf_queue_profiling

#endif
