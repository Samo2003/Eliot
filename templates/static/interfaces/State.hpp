#ifndef ELIOT_STATE_H
#define ELIOT_STATE_H

#include <concepts>

namespace eliot_generated {
    template<typename T>
    concept StateConcept = 
        requires(T state) {
            { state.get_next_packet_state() } -> std::convertible_to<unsigned>;
        };

    template<StateConcept G>
    inline unsigned get_next_state(G& state) noexcept {
        return state.get_next_packet_state();
    }

}

#endif
