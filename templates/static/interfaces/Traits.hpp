#ifndef ELIOT_TRAITS_H
#define ELIOT_TRAITS_H

#include <concepts>
#include <optional>
#include <vector>

namespace eliot_generated {
    template<typename T>
    concept BaseTraitsConcept =
    requires(
        typename T::QueueType q,
        typename T::PacketType p,
        int argc,
        char** argv
    ) {
        typename T::PacketType;
        typename T::QueueType;

        { T::create_queue(argc, argv) } -> std::same_as<typename T::QueueType>;
        
        { T::get_packet(q) } -> std::same_as<std::optional<typename T::PacketType>>;

        { T::accept_packet(q, std::move(p)) } -> std::same_as<void>;

        { T::drop_packet(q, std::move(p)) } -> std::same_as<void>;

        { T::payload(p) } -> std::same_as<const std::vector<uint8_t>&>;

        requires requires { 
            { std::bool_constant<T::modifiable_payload>{} };
        };
    };

    template<typename T>
    concept ModifiablePayloadTraitsConcept =
    requires(typename T::PacketType p) {
        requires (T::modifiable_payload == true);

        { T::mutable_payload(p) } -> std::same_as<std::vector<uint8_t>&>;
    };

    template<typename T>
    concept ImmutablePayloadTraitsConcept =
    requires(
        typename T::PacketType p,
        std::vector<uint8_t> payload
    ) {
        requires (T::modifiable_payload == false);

        { T::change_payload(std::move(p), std::move(payload)) } -> std::same_as<typename T::PacketType>;
    };

    template<typename T>
    concept BackendTraitsConcept = BaseTraitsConcept<T> && (ModifiablePayloadTraitsConcept<T> || ImmutablePayloadTraitsConcept<T>);
}

#endif
