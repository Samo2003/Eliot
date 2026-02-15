#ifndef ELIOT_XOROSHIRO128PLUS_H
#define ELIOT_XOROSHIRO128PLUS_H

#include <stdint.h>

struct xoroshiro128plus {
    using result_type = uint64_t;

    uint64_t s0;
    uint64_t s1;

    static inline uint64_t rotl(uint64_t x, int k) noexcept {
        return (x << k) | (x >> (64 - k));
    }

    explicit xoroshiro128plus(uint64_t seed) noexcept {
        uint64_t x = seed;
        s0 = _splitmix64(x);
        s1 = _splitmix64(x);

        if (s0 == 0 && s1 == 0)
            s1 = 1;
    }

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

    static constexpr result_type min() noexcept { return 0ULL; }
    static constexpr result_type max() noexcept { return UINT64_MAX; }

    inline result_type operator()() noexcept {
        return next();
    }

    private:
        static inline uint64_t _splitmix64(uint64_t& x) noexcept {
            x += 0x9E3779B97F4A7C15ULL;
            uint64_t z = x;
            z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL;
            z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL;
            return z ^ (z >> 31);
        }
};

#endif
