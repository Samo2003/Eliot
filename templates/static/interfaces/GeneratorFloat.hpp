#ifndef ELIOT_GENERATOR_FLOAT_H
#define ELIOT_GENERATOR_FLOAT_H

#include <concepts>

namespace eliot_generated {
    template<typename T>
    concept GeneratorFloatConcept = 
        requires(T gen) {
            { gen.get() } -> std::same_as<float>;
        } || 
        requires {
            { T::get() } -> std::same_as<float>;
        };

    template<GeneratorFloatConcept G>
    inline float generate(G& gen) noexcept {
        return gen.get();
    }

    template<GeneratorFloatConcept G>
    inline float generate() noexcept {
        return G::get();
    }

}

#endif
