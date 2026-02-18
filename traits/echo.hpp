#ifndef ECHO_TRAITS_H
#define ECHO_TRAITS_H

#include "../mocks/echo/nf_queue_echo.hpp"

struct EchoTraits {
    using PacketType = nf_queue_echo::NFQueuePacket;
    using QueueType = nf_queue_echo::NFQueue;

    inline static QueueType create_queue(int argc, char **argv) {
        return QueueType();
    }

    inline static std::optional<PacketType> get_packet(QueueType& q) {
        return q.get_packet();
    }

    inline static void accept_packet(QueueType& q, PacketType&& p) {
        q.accept_packet(std::move(p));
    }

    inline static void drop_packet(QueueType& q, PacketType&& p) {
        q.drop_packet(std::move(p));
    }

    inline static const std::vector<uint8_t>& payload(const PacketType& p) {
        return p.get_payload();
    }

    static constexpr bool modifiable_payload = false;

    inline static PacketType change_payload(PacketType&& old_packet, std::vector<uint8_t>&& new_payload) {
        return PacketType(
            old_packet.get_id(),
            std::move(new_payload),
            *old_packet.get_from()
        );
    }

    inline static PacketType clone(const PacketType& p) {
        return PacketType(
            p.get_id(),
            std::vector<uint8_t>(p.get_payload()),
            *p.get_from()
        );
    }
};

using ActiveTraits = EchoTraits;

#endif
