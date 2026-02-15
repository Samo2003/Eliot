#ifndef ELIOT_TIME_H
#define ELIOT_TIME_H

#include <stdint.h>

#ifndef __APPLE__
#include <time.h>
#else
#include <mach/mach_time.h>
#endif

namespace eliot_generated {
    #ifndef __APPLE__

    inline uint64_t read_clock_ms() {
        static uint64_t factor = (1ull << 32) / 1000000ull;

        struct timespec ts;
        clock_gettime(CLOCK_MONOTONIC_COARSE, &ts);

        uint64_t ns = (uint64_t)ts.tv_sec * 1000000000ull + ts.tv_nsec;
        return (ns * factor) >> 32;
    }

    #else

    inline uint64_t read_clock_ms() {
        static mach_timebase_info_data_t tb = {0};
        if (tb.denom == 0) mach_timebase_info(&tb);

        uint64_t t = mach_absolute_time();
        uint64_t ns = (t * tb.numer) / tb.denom;
        return ns / 1000000ull;
    }

    #endif

    inline uint64_t global_time = 0;
    inline bool time_updated = false;

    inline uint64_t get_global_time() noexcept {
        if (!time_updated) {
            global_time = read_clock_ms();
            time_updated = true;
        }
        return global_time;
    }

}

#endif
