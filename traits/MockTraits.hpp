/**
 * @file MockTraits.hpp
 * @brief Mock backend traits implementation.
 *
 * This backend satisfies eliot_generated::BackendTraitsConcept.
 *
 * The Mock backend is intended for testing and deterministic
 * evaluation scenarios. Packets are loaded from a configuration
 * source and processed without interaction with real networking.
 *
 * Payload is treated as immutable, therefore any modification
 * results in creation of a new PacketType instance.
 *
 * For full interface contract see TraitsTemplate.hpp.
 */

#ifndef MOCK_TRAITS_H
#define MOCK_TRAITS_H

#include <optional>
#include <vector>
#include "../mocks/mock/nf_queue_mock.hpp"

namespace eliot::backend {
    /**
     * @brief Mock backend traits.
     *
     * This backend is intended for deterministic testing scenarios.
     * Packets are obtained from a predefined configuration source
     * instead of a real networking subsystem.
     *
     * Payload is immutable and any modification results
     * in creation of a new PacketType instance.
     */
    struct MockTraits {

        ///> Backend packet representation.
        using PacketType = nf_queue_mock::NFQueuePacket;

        ///> Backend queue implementation.
        using QueueType = nf_queue_mock::NFQueue;

        /**
         * @brief Creates backend queue instance.
         *
         * Expects configuration file path as second argument.
         */
        inline static QueueType create_queue(int argc, char **argv) {
            if (argc < 2)
                throw std::runtime_error("Missing config path");
            return QueueType(argv[1]);
        }

        /**
         * @brief Retrieves next packet from backend queue.
         *
         * @return std::optional containing PacketType if available.
         */
        inline static std::optional<PacketType> get_packet(QueueType& q) {
            return q.get_packet();
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
         * Performs deep copy of payload while preserving metadata.
         */
        inline static PacketType clone(const PacketType& p) {
            return PacketType(
                std::vector<uint8_t>(p.get_payload()),
                p.get_origin()
            );
        }

        /**
         * @brief Returns read-only packet payload reference.
         */
        inline static const std::vector<uint8_t>& payload(const PacketType& p) {
            return p.get_payload();
        }

        ///> Payload is immutable in this backend.
        static constexpr bool modifiable_payload = false;

        /**
         * @brief Returns new packet instance with replaced payload.
         *
         * Used when engine modifies packet payload.
         * Original origin metadata must be preserved.
         */
        inline static PacketType change_payload(PacketType&& old_packet, std::vector<uint8_t>&& new_payload) {
            return PacketType(
                std::move(new_payload),
                old_packet.get_origin()
            );
        }
    };

    ///> Alias used by generated code.
    using ActiveTraits = MockTraits;
}

#endif
