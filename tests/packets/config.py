from pydantic import BaseModel
import json

DEFAULT_CONFIG = "../test_config.json"
DEFAULT_PACKETS = "packets.json"

class Config(BaseModel):
    """Testing configuration representation"""
    listen_ip: str
    listen_port: int
    client_ip: str
    client_port: int
    server_ip: str
    server_port: int

def load_config(config_path: str) -> Config:
    """Loads configuration from `config_path`"""
    try:
        with open(config_path, "r") as file:
            data = json.load(file)
        return Config.model_validate(data)
    except:
        raise RuntimeError("Unable to load packets config")

