#ifndef NF_QUEUE_ECHO_H
#define NF_QUEUE_ECHO_H

#include <cstdint>

#include "core/nf_core.hpp"

namespace nf_queue_echo {

/**
 * @brief NFQueue backend implementation for echo testing mode.
 *
 * This class provides a minimal adapter between the generated
 * processing logic and the NFCore backend implementation.
 */
class NFQueue {
public: 
    /**
     * @brief Construct NFQueue adapter.
     *
     * Default constructor initializes internal NFCore instance.
     */
    explicit NFQueue() {}

    /**
     * @brief Retrieve next available packet from queue.
     *
     * First triggers packet acceptance phase in NFCore,
     * then attempts to pop a packet from internal queue.
     *
     * @return Optional packet if available.
     */
    inline std::optional<NFQueuePacket> get_packet() noexcept {
        _core.accept_packets();
        return _core.queue_pop();
    }

    /**
     * @brief Accept and send packet back through backend.
     *
     * Used when generated logic decides to forward packet.
     */
    inline void accept_packet(NFQueuePacket&& packet) noexcept {
        _core.send(std::move(packet));
    }

    /**
     * @brief Drop packet.
     *
     * In echo testing backend this is a no-op,
     * since packet handling is simulated.
     */
    inline void drop_packet(NFQueuePacket&& /*packet*/) noexcept {}

private:
    ///> Core backend implementation handling low-level operations
    NFCore _core;
};

}   // namespace nf_queue_echo

#endif
