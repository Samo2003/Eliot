#include "PacketProcessor.hpp"
#include <csignal>

using namespace eliot_generated;

int main(int argc, char **argv) {
    std::signal(SIGINT, [](int){
        PacketProcessor<ActiveTraits>::stop();
    });

    try {
        PacketProcessor<ActiveTraits> processor(argc, argv);
        processor.run();
        return EXIT_SUCCESS;
    }
    catch (const std::runtime_error& e) {
        std::cerr << "ERROR: " << e.what() << std::endl;
        return EXIT_FAILURE;
    }
}
