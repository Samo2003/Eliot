#ifndef ELIOT_XOROSHIRO128PLUS_H
#define ELIOT_XOROSHIRO128PLUS_H

#include <stdint.h>

struct xoroshiro128plus {    
    uint64_t s0;
    uint64_t s1;

    static inline uint64_t rotl(uint64_t x, int k) noexcept {
        return (x << k) | (x >> (64 - k));
    }

    explicit xoroshiro128plus(uint64_t seed0, uint64_t seed1) noexcept : s0(seed0), s1(seed1) {}

    inline uint64_t next() noexcept {
        uint64_t result = s0 + s1;

        s1 ^= s0;
        s0 = rotl(s0, 24) ^ s1 ^ (s1 << 16);
        s1 = rotl(s1, 37);

        return result;
    }

    inline uint64_t next_range(uint64_t n) noexcept {
        return (uint64_t)(((__uint128_t)next() * n) >> 64);
    }
};

#endif
