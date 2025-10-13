#include "anchor/nf_queue_mock.hpp"
#include <chrono>
#include <csignal>
#include <iostream>
#include <atomic>

static std::atomic<bool> stop_flag{false};
void handle_sigint(int) { stop_flag = true; }

int main() {
    std::signal(SIGINT, handle_sigint);
    try {
        nf_queue::NFQueue nf;
        std::cout << "Running...\n";
        while (!stop_flag) {
            if (auto maybe_pkt = nf.get_packet()) {
                nf.accept_packet(std::move(*maybe_pkt));
            }
        }
        std::cout << "Exiting\n";
        return EXIT_SUCCESS;
    } catch (const std::runtime_error& e) {
        std::cerr << e.what() << std::endl;
        return EXIT_FAILURE;
    }
}
