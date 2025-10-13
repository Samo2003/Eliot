#ifndef NF_QUEUE_MOCK_H
#define NF_QUEUE_MOCK_H

#include <cstdint>
#include <iostream>
#include <fstream>

#include "core/nf_core.hpp"

namespace nf_queue {
    class NFQueue {
        public: 
            NFQueue() : _core(Config("../mock/test_config.json")) {}

            std::optional<NFQueuePacket> get_packet() noexcept;

            void accept_packet(NFQueuePacket&& packet) noexcept;

            inline void const drop_packet(NFQueuePacket&& packet) noexcept {}

        private:
            NFCore _core;
    };
}

#endif
