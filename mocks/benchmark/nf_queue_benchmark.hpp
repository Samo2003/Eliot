#ifndef NF_QUEUE_PROFILING_H
#define NF_QUEUE_PROFILING_H

#include <optional>
#include <cstdint>
#include <iostream>
#include <vector>
#include <chrono>
#include <numeric>
#include <iomanip>
#include <algorithm>
#include <cmath>
#include "nf_packet.hpp"

namespace nf_queue_benchmark {

/**
 * @brief Synthetic benchmark backend.
 */
class NFQueue {
public: 
    /**
     * @brief Construct profiling backend.
     */
    NFQueue() 
        : _template_payload(_PAYLOAD_SIZE, 0xAB)
    {
        _times.reserve(_RUNS);
    }

    /**
     * @brief Return next synthetic packet.
     *
     * Returns nullopt when limit reached.
     */
    inline std::optional<NFQueuePacket> get_packet() {
        if (_run >= _RUNS) {
            _print_summary();
            throw std::runtime_error("Benchmarking finished");
        }

        if (_processed == 0)
            _start = clock::now();

        if (_processed >= _PACKET_COUNT)
            return std::nullopt;

        ++_processed;
        return NFQueuePacket(_template_payload);
    }

    /**
     * @brief Accepts packet.
     */
    inline void accept_packet(NFQueuePacket&& /*packet*/) noexcept {
        _accepted++;
        _finish_packet();
    }

    /**
     * @brief Drops packet.
     */
    inline void drop_packet(NFQueuePacket&& /*packet*/) noexcept {
        _dropped++;
        _finish_packet();
    }

private:
    using clock = std::chrono::steady_clock;

    ///> Total number of synthetic packets to generate
    static constexpr size_t _PACKET_COUNT = 50000000;

    ///> Total number of runs for benchmarking
    static constexpr size_t _RUNS = 25;

    ///> Total number of warm up runs
    static constexpr size_t _WARMUP_RUNS = 5;

    ///> Payload size for synthetic packet
    static constexpr size_t _PAYLOAD_SIZE = 128;

    ///> Number of bits processed each run
    static constexpr double _BITS_PER_RUN = _PACKET_COUNT * _PAYLOAD_SIZE * 8.0;

    ///> Shared payload buffer reused across all packets
    std::vector<uint8_t> _template_payload;

    ///> Current run number
    size_t _run = 0;

    /// Run statistics
    size_t _processed = 0;
    size_t _accepted = 0;
    size_t _dropped = 0;

    ///> Time measurement
    clock::time_point _start;

    ///> Times per run
    std::vector<double> _times;

    /**
     * @brief Finishes packet after drop or accept and updates statistics
     */
    void _finish_packet() {
        if (_processed != _PACKET_COUNT)
            return;

        if (_run == _WARMUP_RUNS - 1)
            std::cout << "\nWarm-up phase finished (" << _WARMUP_RUNS << " runs). Starting measurements...\n";

        if (_run == _WARMUP_RUNS)
            std::cout << "\n================================ BENCHMARK ================================\n"
                << std::setw(6) << "Run"
                << std::setw(12) << "Time(s)"
                << std::setw(12) << "Accepted"
                << std::setw(12) << "Dropped"
                << std::setw(12) << "PPS (M)"
                << std::setw(12) << "Gbps"
                << std::setw(12) << "Lat (ns)"
                << "\n";

        if (_run >= _WARMUP_RUNS) {
            auto end = clock::now();

            double seconds = std::chrono::duration<double>(end - _start).count();

            double pps = _PACKET_COUNT / seconds;
            double latency_ns = (seconds * 1e9) / _PACKET_COUNT;
            double gbps = _BITS_PER_RUN / seconds / 1e9;

            _times.push_back(seconds);

            // Print run statistics
            std::cout
                << std::setw(6) << (_run - _WARMUP_RUNS + 1)
                << std::setw(12) << std::fixed << std::setprecision(6) << seconds
                << std::setw(12) << _accepted
                << std::setw(12) << _dropped
                << std::setw(12) << std::setprecision(4) << pps / 1e6
                << std::setw(12) << std::setprecision(2) << gbps
                << std::setw(12) << latency_ns
                << "\n";
        }

        _run++;

        // Reset run statistics
        _processed = 0;
        _accepted = 0;
        _dropped = 0;
    }

    /**
     * @brief Prints benchmarking summary
     */
    void _print_summary() const {
        if (_times.empty())
            return;

        double sum = std::accumulate(_times.begin(), _times.end(), 0.0);

        double avg = sum / _times.size();

        double min = *std::min_element(_times.begin(), _times.end());
        double max = *std::max_element(_times.begin(), _times.end());

        double variance = 0;
        for (double t : _times)
            variance += (t - avg) * (t - avg);

        variance /= _times.size();
        double stddev = std::sqrt(variance);

        std::vector<double> sorted = _times;
        std::sort(sorted.begin(), sorted.end());

        double median;
        size_t n = sorted.size();

        if (n % 2 == 0)
            median = (sorted[n/2 - 1] + sorted[n/2]) / 2.0;
        else
            median = sorted[n/2];

        std::cout << "\n============================== SUMMARY ==============================\n";
        std::cout << "Runs: " << _times.size() << "\n";
        std::cout << "Packets/run: " << _PACKET_COUNT << "\n";
        std::cout << "Average: " << std::setprecision(6) << avg << " s\n";
        std::cout << "Median: " << median << " s\n";
        std::cout << "Min: " << min << " s\n";
        std::cout << "Max: " << max << " s\n";
        std::cout << "StdDev: " << stddev << " s\n";

        double pps_m = _PACKET_COUNT / avg / 1e6;
        double gbps = _BITS_PER_RUN / avg / 1e9;

        double median_pps_m = _PACKET_COUNT / median / 1e6;
        double median_gbps = _BITS_PER_RUN / median / 1e9;

        std::cout << "Throughput: " << std::setprecision(4) << pps_m << " M packets/sec\n";
        std::cout << "Throughput: " << gbps << " Gbps\n";

        std::cout << "Median throughput: " << median_pps_m << " M packets/sec\n";
        std::cout << "Median throughput: " << median_gbps << " Gbps\n";
    }
};

}   // namespace nf_queue_benchmark

#endif
