from __future__ import annotations
import ipaddress
from typing import Literal
from pydantic import model_validator
from .base import ConditionBase

class IP(ConditionBase[Literal["IP"]]):
    """
    Check IP address
    """

    # Destination or source IP address
    ip: str | None = None

    # Source IP address
    src: str | None = None

    # Destination IP address
    dst: str | None = None

    @model_validator(mode="after")
    def validate_ips(self) -> IP:
        ips = [ip for ip in [self.ip, self.src, self.dst] if ip is not None]

        if not ips:
            raise ValueError("not ips provided")

        if self.ip is not None:
            if self.src is not None or self.dst is not None:
                raise ValueError("when ip is provided src and dst cannot be given")

        for ip in ips:
            try:
                ipaddress.ip_address(ip)
            except ValueError:
                raise ValueError(f"invalid ip address provided: {ip}")
            
        if self.src is not None and self.dst is not None:
            if ipaddress.ip_address(self.src).version != ipaddress.ip_address(self.dst).version:
                raise ValueError("src and dst must have the same IP version")

        return self
    
    def cpp_type(self) -> str:
        parts = [super().cpp_type_base()]

        if self.src is not None:
            parts.append(f"src_{self.src.replace('.', '_').replace(':', '_')}")

        if self.dst is not None:
            parts.append(f"dst_{self.dst.replace('.', '_').replace(':', '_')}")
        
        return "_".join(parts)
    
    def convert(self, ip: str) -> bytes:
        """Converts ip string to bytes"""
        return ipaddress.ip_address(ip).packed
    
    def ipv4(self) -> bool:
        """Determines if condition is checking IPv4 or IPv6 packets"""
        if self.ip is not None:
            return ipaddress.ip_address(self.ip).version == 4
        if self.src is not None:
            return ipaddress.ip_address(self.src).version == 4
        if self.dst is not None:
            return ipaddress.ip_address(self.dst).version == 4
        return False
