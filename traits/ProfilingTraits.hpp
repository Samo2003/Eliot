/**
 * @file ProfilingTraits.hpp
 * @brief Profiling backend traits implementation.
 *
 * This backend satisfies eliot_generated::BackendTraitsConcept.
 *
 * PacketType is a lightweight wrapper referencing external payload.
 * Payload is directly modifiable.
 *
 * For full interface description see TraitsTemplate.hpp.
 */

#ifndef PROFILING_TRAITS_H
#define PROFILING_TRAITS_H

#include <optional>
#include "../mocks/profiling/nf_queue_profiling.hpp"

/**
 * @brief Profiling backend traits.
 *
 * This backend is optimized for performance profiling.
 * PacketType is a lightweight wrapper referencing external payload.
 *
 * Payload is directly modifiable (no local copy is required).
 */
struct ProfilingTraits {

    ///> Backend packet representation.
    using PacketType = nf_queue_profiling::NFQueuePacket;

    ///> Backend queue implementation.
    using QueueType = nf_queue_profiling::NFQueue;

    /**
     * @brief Creates backend queue.
     */
    inline static QueueType create_queue(int argc, char **argv) {
        return QueueType();
    }

    /**
     * @brief Retrieves next packet from queue.
     *
     * Returns std::nullopt if no packet is available.
     */
    inline static std::optional<PacketType> get_packet(QueueType& q) {
        if (auto* p = q.get_packet())
            return std::optional<PacketType>(std::move(*p));
        return std::nullopt;
    }

    /**
     * @brief Forwards packet to backend.
     */
    inline static void accept_packet(QueueType& q, PacketType&& p) {
        q.accept_packet(std::move(p));
    }

    /**
     * @brief Drops packet in backend.
     */
    inline static void drop_packet(QueueType& q, PacketType&& p) {
        q.drop_packet(std::move(p));
    }

    /**
     * @brief Creates packet clone.
     *
     * In profiling backend clone shares underlying payload reference.
     */
    inline static PacketType clone(const PacketType& p) {
        return PacketType(p.get_payload());
    }

    /**
     * @brief Returns read-only packet payload.
     */
    inline static const std::vector<uint8_t>& payload(const PacketType& p) {
        return p.get_payload();
    }

    ///> Indicates direct payload modification is supported.
    static constexpr bool modifiable_payload = true;

    /**
     * @brief Returns mutable reference to payload buffer.
     */
    inline static std::vector<uint8_t>& mutable_payload(PacketType& p) {
        return p.get_payload();
    }
};

using ActiveTraits = ProfilingTraits;

#endif
