from pydantic import BaseModel
import json

class Config(BaseModel):
    listen_ip: str
    listen_port: int
    client_ip: str
    client_port: int
    server_ip: str
    server_port: int

def load_config(config_path: str) -> Config:
    try:
        with open(config_path, "r") as file:
            data = json.load(file)
        config = Config(**data)
    except:
        raise RuntimeError("Unable to load packets config")
    
    return config
