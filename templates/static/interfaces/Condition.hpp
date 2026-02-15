#ifndef ELIOT_CONDITION_H
#define ELIOT_CONDITION_H

#include "../../Packet.hpp"
#include <concepts>

namespace eliot_generated {
    template<typename T>
    concept ConditionConcept = 
        requires(T condition, const Packet* packet) {
            { condition.fulfilled(packet) } -> std::convertible_to<bool>;
        } || 
        requires(const Packet* packet) {
            { T::fulfilled(packet) } -> std::convertible_to<bool>;
        };

    template<ConditionConcept C>
    inline bool evaluate_condition(C& condition, const Packet* packet) noexcept {
        return condition.fulfilled(packet);
    }

    template<ConditionConcept C>
    inline bool evaluate_condition(const Packet* packet) noexcept {
        return C::fulfilled(packet);
    }
}

#endif
