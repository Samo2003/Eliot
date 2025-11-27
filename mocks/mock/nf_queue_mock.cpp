#include "nf_queue_mock.hpp"

namespace nf_queue_mock {
    void NFQueue::accept_packet(NFQueuePacket&& packet) noexcept {
        if (packet.get_origin() == Origin::Client) {
            _core.send_to_server(packet.get_payload());
        } else if (packet.get_origin() == Origin::Server) {
            _core.send_to_client(packet.get_payload());
        }
    }
}
