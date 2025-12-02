#ifndef ELIOT_CALENDAR_H
#define ELIOT_CALENDAR_H

#include <vector>
#include <optional>
#include <array>
#include "../Time.hpp"
#include "../Bucket.hpp"

namespace eliot_generated {
    struct Calendar {
        void schedule(Packet* packet, uint64_t delay) noexcept;

        Packet* get_ready() noexcept;

        inline bool empty() const noexcept { return _size == 0; }

        private:
            static constexpr uint32_t _SLOTS = 256;
            static constexpr uint64_t _MASK = _SLOTS - 1;

            static constexpr uint64_t _L0_SPAN = _SLOTS;
            static constexpr uint64_t _L1_SPAN = _SLOTS * _SLOTS;
            static constexpr uint64_t _L2_SPAN = _L1_SPAN * _SLOTS;

            size_t _size = 0;
            uint64_t _start = read_clock_ms();
            uint64_t _current_tick = 0;
        
            struct CalendarItem {
                uint64_t tick;
                Packet* packet;
                CalendarItem* next = nullptr;
            };

            using BucketT = Bucket<CalendarItem>;

            std::array<BucketT, _SLOTS> _wheel0{};
            std::array<BucketT, _SLOTS> _wheel1{};
            std::array<BucketT, _SLOTS> _wheel2{};

            void _cascade_from_L1() noexcept;
            void _cascade_from_L2() noexcept;
            
            inline uint64_t _current_tick_from_clock() const noexcept {
                uint64_t now = get_global_time();
                return now < _start ? _current_tick : now - _start;
            }
    };
}

#endif
