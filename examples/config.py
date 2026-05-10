from pathlib import Path
import json
from pydantic import BaseModel

CONFIG_PATH = Path(__file__).parent / "backend_config.json"

class Config(BaseModel):
    """Testing configuration representation"""
    eliot_ip: str
    eliot_port: int
    client_ip: str
    client_port: int
    server_ip: str
    server_port: int

def load_config() -> Config:
    """Loads configuration"""
    try:
        with open(CONFIG_PATH, "r") as file:
            data = json.load(file)
        return Config.model_validate(data)
    except Exception as e:
        raise RuntimeError("Unable to load packets config") from e
