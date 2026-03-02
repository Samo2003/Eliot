#include "nf_queue_mock.hpp"

namespace nf_queue_mock {

/**
 * @brief Process accepted packet according to its origin.
 *
 * Based on packet origin, payload is forwarded
 * to the opposite endpoint.
 */
void NFQueue::accept_packet(NFQueuePacket&& packet) noexcept {
    if (packet.get_origin() == NFQueuePacket::Origin::Client) {
        // Forward client packet to server side
        _core.send_to_server(packet.get_payload());
    } else if (packet.get_origin() == NFQueuePacket::Origin::Server) {
        // Forward server packet to client side
        _core.send_to_client(packet.get_payload());
    }
}

}   // namespace nf_queue_mock
