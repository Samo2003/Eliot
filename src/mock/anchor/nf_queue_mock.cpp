#include "nf_queue_mock.hpp"

namespace nf_queue {
    std::optional<NFQueuePacket> NFQueue::get_packet() noexcept {
        _core.accept_packets();
        return _core.queue_pop();
    }

    void NFQueue::accept_packet(NFQueuePacket&& packet) noexcept {
        if (packet.get_origin() == Origin::Client) {
            _core.send_to_server(packet.get_payload());
        } else if (packet.get_origin() == Origin::Server) {
            _core.send_to_client(packet.get_payload());
        }
    }
}
