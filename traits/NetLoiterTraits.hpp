/**
 * @file NetLoiterTraits.hpp
 * @brief NetLoiter NFQUEUE backend traits implementation.
 *
 * This backend satisfies eliot::core::BackendTraitsConcept.
 *
 * The NetLoiter backend provides integration with Linux NFQUEUE
 * using the nf_queue library.
 *
 * Packet ownership is represented using std::unique_ptr,
 * while the underlying packet type is immutable.
 * Any payload modification results in creation of a new packet instance.
 *
 * For full interface contract see TraitsTemplate.hpp.
 */

#ifndef ELIOT_TRAITS_TEMPLATE_H
#define ELIOT_TRAITS_TEMPLATE_H

#include <optional>
#include <vector>
#include "../../NetLoiter/include/nf_queue/nf_queue.hpp"

namespace eliot::backend {

/**
 * @brief NetLoiter backend traits.
 *
 * This backend provides real packet processing using NFQUEUE.
 *
 * Packets are represented as owning handles (std::unique_ptr),
 * ensuring efficient transfer of ownership without copying.
 *
 * The underlying packet type is immutable — payload modifications
 * are implemented by constructing a new packet instance.
 */
struct NetLoiterTraits {

    ///> Backend queue implementation based on NFQUEUE.
    using QueueType = nf_queue::NFQueue<true>;

    ///> Backend packet representation.
    using PacketType = typename QueueType::TNFQueuePacket;

    /**
     * @brief Creates backend queue instance.
     *
     * Initializes NFQUEUE with predefined queue number and mark.
     */
    static QueueType create_queue(int argc, char** argv) {
        nf_queue::QueueNumber queue_number = 1;
        nf_queue::MarkNumber mark_ignore = 1;
        return QueueType(queue_number, mark_ignore);
    }

    /**
     * @brief Retrieves next packet from backend queue.
     *
     * Transfers ownership of packet from NFQUEUE to the caller.
     *
     * @return std::optional containing PacketType if available.
     */
    static std::optional<PacketType> get_packet(QueueType& q) {
        auto p = q.get_packet();
        if (!p) return std::nullopt;
        return std::move(p);
    }

    /**
     * @brief Forwards packet to backend.
     *
     * Consumes PacketType and transfers ownership back to NFQUEUE.
     */
    static void accept_packet(QueueType& q, PacketType&& p) {
        q.accept_packet(std::move(*p));
    }

    /**
     * @brief Drops packet in backend.
     *
     * Consumes PacketType and issues drop verdict.
     */
    static void drop_packet(QueueType& q, PacketType&& p) {
        q.drop_packet(std::move(*p));
    }

    /**
     * @brief Creates packet clone.
     *
     * Performs deep copy of underlying packet while preserving metadata.
     */
    static PacketType clone(const PacketType& p) {
        return std::make_unique<nf_queue::NFQueuePacket>(
            nf_queue::NFQueuePacketPayload(p->get_payload()),
            p->get_id(),
            p->get_outdev(),
            nf_queue::MacAddress(p->get_dst_mac())
        );
    }

    /**
     * @brief Returns read-only packet payload reference.
     */
    static const std::vector<uint8_t>& payload(const PacketType& p) {
        return p->get_payload();
    }

    ///> Payload is immutable in this backend.
    static constexpr bool modifiable_payload = false;

    /**
     * @brief Returns new packet instance with replaced payload.
     *
     * Used by the engine when payload modifications are required.
     * The original packet remains unchanged and all metadata is preserved.
     */
    static PacketType change_payload(PacketType&& old_packet, std::vector<uint8_t>&& new_payload) {
        return std::make_unique<nf_queue::NFQueuePacket>(
            std::move(new_payload),
            old_packet->get_id(),
            old_packet->get_outdev(),
            nf_queue::MacAddress(old_packet->get_dst_mac())
        );
    }
};

///> Alias used by generated code.
using ActiveTraits = NetLoiterTraits;

}   // namespace eliot::backend

#endif
