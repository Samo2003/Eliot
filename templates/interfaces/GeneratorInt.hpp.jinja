#ifndef ELIOT_GENERATOR_INT_H
#define ELIOT_GENERATOR_INT_H

#include <concepts>

namespace eliot_generated {
    template<typename T>
    concept GeneratorIntConcept = 
        requires(T gen) {
            { gen.get() } -> std::same_as<int>;
        } || 
        requires {
            { T::get() } -> std::same_as<int>;
        };

    template<GeneratorIntConcept G>
    inline int generate(G& gen) noexcept {
        return gen.get();
    }

    template<GeneratorIntConcept G>
    inline int generate() noexcept {
        return G::get();
    }

}

#endif
