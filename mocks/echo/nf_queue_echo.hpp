#ifndef NF_QUEUE_ECHO_H
#define NF_QUEUE_ECHO_H

#include <cstdint>

#include "core/nf_core.hpp"

namespace nf_queue_echo {
    class NFQueue {
        public: 
            explicit NFQueue() {}

            inline std::optional<NFQueuePacket> get_packet() noexcept {
                _core.accept_packets();
                return _core.queue_pop();
            }

            inline void accept_packet(NFQueuePacket&& packet) noexcept {
                _core.send(std::move(packet));
            }

            inline void drop_packet(NFQueuePacket&& packet) noexcept {}

        private:
            NFCore _core;
    };
}

#endif
