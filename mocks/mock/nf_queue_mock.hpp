#ifndef NF_QUEUE_MOCK_H
#define NF_QUEUE_MOCK_H

#include <cstdint>
#include <iostream>
#include <fstream>

#include "core/nf_core.hpp"

namespace nf_queue_mock {

/**
 * @brief Mock NFQueue backend.
 *
 * This backend extends NFCore with configurable behavior
 * defined by external configuration file.
 */
class NFQueue {
public:
    /**
     * @brief Construct mock backend with configuration file.
     *
     * @param config_path Path to backend configuration file.
     */
    NFQueue(const std::string& config_path) : _core(Config(config_path)) {}

    /**
     * @brief Retrieve next packet from backend queue.
     *
     * Internally triggers packet reception before polling queue.
     */
    inline std::optional<NFQueuePacket> get_packet() noexcept {
        _core.accept_packets();
        return _core.queue_pop();
    }

    /**
     * @brief Accept packet.
     */
    void accept_packet(NFQueuePacket&& packet) noexcept;

    /**
     * @brief Drop packet.
     *
     * Implemented as no-op.
     */
    inline void drop_packet(NFQueuePacket&& /*packet*/) noexcept {}

private:
    ///> Core backend engine with configuration support
    NFCore _core;
};

}   // namespace nf_queue_mock

#endif
