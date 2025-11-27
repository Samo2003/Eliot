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
        static double factor = 0.0;

        if (factor == 0.0) {
            mach_timebase_info(&tb);
            factor = (double)tb.numer / (double)tb.denom / 1000000.0;
        }

        return (uint64_t)(mach_absolute_time() * factor);
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
