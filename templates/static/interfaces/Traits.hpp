#ifndef ELIOT_TRAITS_H
#define ELIOT_TRAITS_H

#include <concepts>
#include <optional>
#include <vector>

namespace eliot_generated {

    /**
     * @brief Base requirements for backend traits.
     *
     * Defines mandatory types and functions required
     * for packet acquisition, forwarding and inspection.
     *
     * @tparam T Traits implementation.
     */
    template<typename T>
    concept BaseTraitsConcept =
        requires(
            typename T::QueueType q,
            typename T::PacketType p,
            const typename T::PacketType cp,
            int argc,
            char** argv
        ) {
            typename T::PacketType;
            typename T::QueueType;

            // Queue creation
            { T::create_queue(argc, argv) } -> std::same_as<typename T::QueueType>;
            
            // Packet retrieval
            { T::get_packet(q) } -> std::same_as<std::optional<typename T::PacketType>>;

            // Packet forwarding
            { T::accept_packet(q, std::move(p)) } -> std::same_as<void>;

            // Packet dropping
            { T::drop_packet(q, std::move(p)) } -> std::same_as<void>;

            // Read-only payload access
            { T::payload(p) } -> std::same_as<const std::vector<uint8_t>&>;

            // Compile-time payload mutability flag
            requires requires { 
                { std::bool_constant<T::modifiable_payload>{} };
            };

            // Packet cloning
            { T::clone(cp) } -> std::same_as<typename T::PacketType>;
        };

    /**
     * @brief Traits with directly modifiable payload.
     *
     * Requires mutable access to payload.
     */
    template<typename T>
    concept ModifiablePayloadTraitsConcept =
        requires(typename T::PacketType p) {
            requires (T::modifiable_payload == true);

            { T::mutable_payload(p) } -> std::same_as<std::vector<uint8_t>&>;
        };

    /**
     * @brief Traits with immutable payload.
     *
     * Requires payload replacement function instead
     * of direct mutation.
     */
    template<typename T>
    concept ImmutablePayloadTraitsConcept =
        requires(
            typename T::PacketType p,
            std::vector<uint8_t> payload
        ) {
            requires (T::modifiable_payload == false);

            { T::change_payload(std::move(p), std::move(payload)) } -> std::same_as<typename T::PacketType>;
        };

    /**
     * @brief Complete backend traits concept.
     *
     * Combines base requirements with exactly one
     * payload handling strategy.
     */
    template<typename T>
    concept BackendTraitsConcept = BaseTraitsConcept<T> && (ModifiablePayloadTraitsConcept<T> || ImmutablePayloadTraitsConcept<T>);
}

#endif
