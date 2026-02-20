/**
 * @file EchoTraits.hpp
 * @brief Echo backend traits implementation.
 *
 * This backend satisfies eliot_generated::BackendTraitsConcept.
 *
 * The Echo backend simulates NFQUEUE behavior for testing purposes.
 * Payload is treated as immutable, therefore packet modification
 * is performed by creating a new PacketType instance.
 *
 * For full interface contract see TraitsTemplate.hpp.
 */

#ifndef ECHO_TRAITS_H
#define ECHO_TRAITS_H

#include "../mocks/echo/nf_queue_echo.hpp"

namespace eliot::backend {
    /**
     * @brief Echo backend traits.
     *
     * This backend simulates echo-like NFQUEUE behavior
     * for testing and validation purposes.
     *
     * Payload is immutable and any modification results
     * in creation of a new PacketType instance.
     */
    struct EchoTraits {

        ///> Backend packet representation.
        using PacketType = nf_queue_echo::NFQueuePacket;

        ///> Backend queue implementation.
        using QueueType = nf_queue_echo::NFQueue;

        /**
         * @brief Creates backend queue instance.
         */
        inline static QueueType create_queue(int argc, char **argv) {
            return QueueType();
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
                *p.get_from()
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
         * Used by engine when payload modifications are required.
         * The original packet metadata must be preserved for backend requirements.
         */
        inline static PacketType change_payload(PacketType&& old_packet, std::vector<uint8_t>&& new_payload) {
            return PacketType(
                std::move(new_payload),
                *old_packet.get_from()
            );
        }
    };

    ///> Alias used by generated code.
    using ActiveTraits = EchoTraits;
}

#endif
