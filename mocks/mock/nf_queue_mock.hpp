#ifndef NF_QUEUE_MOCK_H
#define NF_QUEUE_MOCK_H

#include <cstdint>
#include <iostream>
#include <fstream>

#include "core/nf_core.hpp"

namespace nf_queue_mock {
    class NFQueue {
        public: 
            NFQueue(const std::string& config_path) : _core(Config(config_path)) {}

            inline std::optional<NFQueuePacket> get_packet() noexcept {
                _core.accept_packets();
                return _core.queue_pop();
            }

            void accept_packet(NFQueuePacket&& packet) noexcept;

            inline void drop_packet(NFQueuePacket&& packet) noexcept {}

        private:
            NFCore _core;
    };
}

#endif
