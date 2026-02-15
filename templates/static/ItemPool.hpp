#ifndef ELIOT_ITEMPOOL_H
#define ELIOT_ITEMPOOL_H

#include <cstddef>
#include <new>
#include <utility>
#include <cstdint>

namespace eliot_generated {
    template <typename T, size_t CHUNK_SIZE = 4096>
    struct ItemPool {
        public:
            ItemPool() = default;
            ItemPool(const ItemPool&) = delete;
            ItemPool& operator=(const ItemPool&) = delete;

            ~ItemPool() {
                while(_chunks) {
                    Chunk* c = _chunks;
                    _chunks = _chunks->next;
                    ::operator delete(c);
                }
            }

            template<typename... Args>
            inline T* acquire(Args&&... args) {
                if (!_free) 
                    _allocate_chunk();

                Node* n = _free;
                _free = n->next;

                T* item = reinterpret_cast<T*>(n);

                return ::new (item) T(std::forward<Args>(args)...);
            }

            inline void release(T* item) noexcept {
                if (!item)
                    return;

                item->~T();

                Node* n = reinterpret_cast<Node*>(item);

                n->next = _free;
                _free = n;
            }

        private:

            struct Node {
                Node* next;
            };

            struct Chunk {
                Chunk* next;
                alignas(T) uint8_t storage[sizeof(T) * CHUNK_SIZE];
            };

            Node* _free = nullptr;

            Chunk* _chunks = nullptr;

            inline void _allocate_chunk() {
                Chunk* c = static_cast<Chunk*>(::operator new(sizeof(Chunk)));

                c->next = _chunks;
                _chunks = c;

                for (size_t i = 0; i < CHUNK_SIZE; i++) {
                    uint8_t *ptr = c->storage + i * sizeof(T);

                    Node* n = reinterpret_cast<Node*>(ptr);
                    n->next = _free;
                    _free = n;
                }
            }
    };
}

#endif
