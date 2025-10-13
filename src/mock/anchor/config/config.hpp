#ifndef CONFIG_H
#define CONFIG_H

#include <string>
#include <fstream>
#include <sstream>
#include <stdexcept>

namespace nf_queue {
    class Config {
        public:
            explicit Config(const std::string& config_path);

            std::string listen_ip;
            uint16_t listen_port;
            std::string client_ip;
            uint16_t client_port;
            std::string server_ip;
            uint16_t server_port;

        private:
            static std::string _get_value(const std::string& config_file, const std::string& key);

    };
}

#endif
