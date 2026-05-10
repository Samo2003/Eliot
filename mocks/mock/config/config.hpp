#ifndef CONFIG_H
#define CONFIG_H

#include <string>
#include <fstream>
#include <sstream>
#include <stdexcept>
#include <cstdint>
#include <cctype>

namespace nf_queue_mock {

/**
 * @brief Configuration loader for mock backend.
 */
class Config {
public:
    /**
     * @brief Construct configuration from file path.
     *
     * @param config_path Path to configuration file
     *
     * @throw std::runtime_error on parsing failure.
     */
    explicit Config(const std::string& config_path);

    ///> IP address to bind listening socket
    std::string eliot_ip;

    ///> Port to bind listening socket
    uint16_t eliot_port;

    ///> Client endpoint IP
    std::string client_ip;

    ///> Client endpoint port
    uint16_t client_port;

    ///> Server endpoint IP
    std::string server_ip;

    ///> Server endpoint port
    uint16_t server_port;

private:
    /**
     * @brief Extract value associated with given key from config file.
     *
     * @param config_file Full file content
     * @param key Configuration key
     *
     * @return Parsed string value
     *
     * @throw std::runtime_error if key not found.
     */
    static std::string _get_value(const std::string& config_file, const std::string& key);
};

}   // namespace nf_queue_mock

#endif
