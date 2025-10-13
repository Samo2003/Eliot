#ifndef NF_CORE_H
#define NF_CORE_H

#include <arpa/inet.h>
#include <fcntl.h>
#include <netinet/in.h>
#include <optional>

#include "../config/config.hpp"
#include "socket.hpp"
#include "nf_packet.hpp"

namespace nf_queue {
    class NFCore {
        public:
            explicit NFCore(const Config& config) 
                : _receive_socket(_make_recv_socket(config.listen_ip, config.listen_port)),
                _send_socket(_make_send_socket()) {
                    _translate_address(config.client_ip, config.client_port, _client_addr);
                    _translate_address(config.server_ip, config.server_port, _server_addr);  
                }

            void accept_packets(void) noexcept;

            inline const bool send_to_client(const std::vector<uint8_t>& data) const noexcept {
                ssize_t n = sendto(_send_socket.get(), data.data(), data.size(), 0, reinterpret_cast<const sockaddr*>(&_client_addr), sizeof(_client_addr));
                return n == data.size();
            }

            inline const bool send_to_server(const std::vector<uint8_t>& data) const noexcept {
                ssize_t n = sendto(_send_socket.get(), data.data(), data.size(), 0, reinterpret_cast<const sockaddr*>(&_server_addr), sizeof(_server_addr));
                return n == data.size();
            }
            
            std::optional<NFQueuePacket> queue_pop(void) noexcept;

        private:
            Socket _receive_socket;
            Socket _send_socket;
            sockaddr_in _client_addr{};
            sockaddr_in _server_addr{};
            uint64_t _packet_id = 1;
            std::queue<NFQueuePacket> _queue;

            static Socket _make_recv_socket(const std::string& bind_addr, uint16_t port);
            static Socket _make_send_socket(void);
            static void _translate_address(const std::string& ip, uint16_t port, sockaddr_in& addr);
    };
}

#endif
