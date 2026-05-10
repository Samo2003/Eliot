#include "config.hpp"

namespace nf_queue_mock {

/**
 * @brief Construct configuration object from JSON file.
 */
Config::Config(const std::string& config_path) {
    std::ifstream ifs(config_path);
    if (!ifs)
        throw std::runtime_error("Failed to open config file");

    std::stringstream buffer;
    buffer << ifs.rdbuf();
    std::string config_file = buffer.str();

    eliot_ip = _get_value(config_file, "eliot_ip");
    eliot_port = static_cast<uint16_t>(std::stoi(_get_value(config_file, "eliot_port")));
    client_ip = _get_value(config_file, "client_ip");
    client_port = static_cast<uint16_t>(std::stoi(_get_value(config_file, "client_port")));
    server_ip = _get_value(config_file, "server_ip");
    server_port = static_cast<uint16_t>(std::stoi(_get_value(config_file, "server_port")));

}  

/**
 * @brief Extract value for given key from JSON.
 */
std::string Config::_get_value(const std::string& config_file, const std::string& key) {
    // Locate key in file
    size_t pos = config_file.find("\"" + key + "\"");
    if (pos == std::string::npos)
        throw std::runtime_error(key + " not found in config file");

    // Find ':' separator
    pos = config_file.find(':', pos);
    if (pos == std::string::npos)
        throw std::runtime_error("Invalid format for key: " + key);

    pos++;
    // Skip whitespace
    while (pos < config_file.size() && isspace(config_file[pos]))
        pos++;

    // String value
    if (config_file[pos] == '"') {
        size_t end = config_file.find('"', pos + 1);
        return config_file.substr(pos + 1, end - pos -1);
    // Numeric value
    } else {
        size_t end = config_file.find(",", pos);
        return config_file.substr(pos, end - pos);
    }
}

}   // namespace nf_queue_mock
