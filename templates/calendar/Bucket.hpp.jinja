#ifndef ELIOT_BUCKET_H
#define ELIOT_BUCKET_H

#include <stdint.h>
#include "../Packet.hpp"

namespace eliot_generated {
    template<typename T>
    concept BucketItem = requires(T* item) {
        { item->packet } -> std::convertible_to<Packet*>;
        { item->next }   -> std::convertible_to<T*>;
    };

    template<BucketItem Item>
    struct Bucket {
        inline void push(Item* item) noexcept {
            item->next = nullptr;
            if (_tail) {
                _tail->next = item;
            } else {
                _head = item;
            }
            _tail = item;
        }

        inline Item* pop() noexcept {
            if (!_head) 
                return nullptr;
            Item* item = _head;
            _head = _head->next;
            if (!_head) 
                _tail = nullptr;
            return item;
        }

        ~Bucket() noexcept {
            Item* item = _head;
            while (item) {
                Item* next = item->next;
                delete item->packet;
                delete item;
                item = next;
            }
        }
        
        private:
            Item* _head = nullptr;
            Item* _tail = nullptr;
    };
}

#endif
