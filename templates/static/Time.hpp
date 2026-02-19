#ifndef ELIOT_TIME_H
#define ELIOT_TIME_H

#include <stdint.h>

#ifndef __APPLE__
#include <time.h>
#else
#include <mach/mach_time.h>
#endif

namespace eliot_generated {
    struct Time {
        static inline uint64_t now() noexcept {
            if (!_updated) {
                _global_time = _read_clock_ms();
                _updated = true;
            }
            return _global_time;
        }

        static inline void reset() {
            _updated = false;
        }

        private:
            inline static uint64_t _global_time = 0;
            inline static bool _updated = false;

            static inline uint64_t _read_clock_ms() {
#ifndef __APPLE__
                static uint64_t factor = (1ull << 32) / 1000000ull;

                struct timespec ts;
                clock_gettime(CLOCK_MONOTONIC_COARSE, &ts);

                uint64_t ns = (uint64_t)ts.tv_sec * 1000000000ull + ts.tv_nsec;
                return (ns * factor) >> 32;
#else
                static mach_timebase_info_data_t tb = {0};
                if (tb.denom == 0) mach_timebase_info(&tb);

                uint64_t t = mach_absolute_time();
                uint64_t ns = (t * tb.numer) / tb.denom;
                return ns / 1000000ull;
#endif
            }
    };
}

#endif
