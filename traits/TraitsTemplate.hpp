/**
 * @file TraitsTemplate.hpp
 * @brief Template for implementing a custom backend for Eliot.
 *
 * This file defines the required interface for backend traits used by
 * the generated packet processor.
 *
 * A traits structure must satisfy eliot_generated::BackendTraitsConcept.
 *
 * The runtime engine relies entirely on this interface for:
 *  - packet acquisition
 *  - packet forwarding or dropping
 *  - packet cloning
 *  - payload access and modification
 *
 * The traits layer represents a compile-time boundary between
 * the generic fault injector and a concrete packet backend.
 * 
 * The traits file must define:
 *
 *     using ActiveTraits = YourTraitsType;
 *
 * This alias is used by the generated code.
 * 
 * Example implementations can be found in:
 *  - MockTraits.hpp
 *  - EchoTraits.hpp
 *  - ProfilingTraits.hpp
 */

#ifndef ELIOT_TRAITS_TEMPLATE_H
#define ELIOT_TRAITS_TEMPLATE_H

#include <optional>
#include <vector>
#include "your_backend.hpp"

/**
 * @brief Template for implementing custom backend traits.
 *
 * Replace PacketType and QueueType with backend-specific types.
 *
 * - get_packet()
 *      - Must return ownership of a PacketType instance.
 *      - std::nullopt indicates no packet available.
 *
 * - accept_packet() / drop_packet()
 *      - Must consume PacketType (rvalue).
 *      - PacketType must not be used after forwarding.
 *
 * - clone()
 *      - Must return a semantically valid duplicate of PacketType.
 *      - Deep copy or shallow copy semantics are backend-defined.
 */
struct TraitsTemplate {

    ///> Backend packet representation.
    ///> Must be move-constructible and destructible.
    using PacketType = /* your packet type */;

    ///> Backend queue implementation.
    using QueueType = /* your queue type */;

    /**
     * @brief Creates backend queue instance.
     *
     * Called once during PacketProcessor construction.
     */
    static QueueType create_queue(int argc, char** argv);

    /**
     * @brief Retrieves next packet from backend.
     *
     * @return std::optional containing PacketType if available.
     */
    static std::optional<PacketType> get_packet(QueueType& q);

    /**
     * @brief Forwards packet to backend.
     *
     * Consumes PacketType instance.
     */
    static void accept_packet(QueueType& q, PacketType&& p);

    /**
     * @brief Drops packet in backend.
     *
     * Consumes PacketType instance.
     */
    static void drop_packet(QueueType& q, PacketType&& p);

    /**
     * @brief Creates packet clone.
     *
     * Used internally by the engine during model evaluation.
     */
    static PacketType clone(const PacketType& p);

    /**
     * @brief Returns read-only payload reference.
     *
     * Must return reference to payload buffer.
     */
    static const std::vector<uint8_t>& payload(const PacketType& p);

    /**
     * @brief Payload handling strategy selector.
     *
     * Set to true  -> implement mutable_payload()
     * Set to false -> implement change_payload()
     */
    static constexpr bool modifiable_payload = /* true or false */;

    /**
     * @brief Returns mutable reference to payload.
     *
     * Implement only if modifiable_payload == true.
     */
    static std::vector<uint8_t>& mutable_payload(PacketType& p);

    /**
     * @brief Returns new packet with replaced payload.
     *
     * Implement only if modifiable_payload == false.
     *
     * Must return a new PacketType instance with modified payload.
     */
    static PacketType change_payload(PacketType&& old_packet, std::vector<uint8_t>&& new_payload);
};

///> Alias used by generated code.
using ActiveTraits = TraitsTemplate;

#endif
