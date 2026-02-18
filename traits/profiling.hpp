#ifndef PROFILING_TRAITS_H
#define PROFILING_TRAITS_H

#include <optional>
#include "../mocks/profiling/nf_queue_profiling.hpp"

struct ProfilingTraits {
    using PacketType = nf_queue_profiling::NFQueuePacket;
    using QueueType = nf_queue_profiling::NFQueue;

    inline static QueueType create_queue(int argc, char **argv) {
        return QueueType();
    }

    inline static std::optional<PacketType> get_packet(QueueType& q) {
        if (auto* p = q.get_packet())
            return std::optional<PacketType>(std::move(*p));
        return std::nullopt;
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

    static constexpr bool modifiable_payload = true;

    inline static std::vector<uint8_t>& mutable_payload(PacketType& p) {
        return p.get_payload();
    }
};

using ActiveTraits = ProfilingTraits;

#endif
