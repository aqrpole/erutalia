"""
ULID generation utilities
"""
import ulid
from typing import Optional

def generate_ulid() -> str:
    """Generate a ULID string"""
    return str(ulid.new())

def generate_ulid_bytes() -> bytes:
    """Generate ULID as bytes"""
    return ulid.new().bytes

def parse_ulid(ulid_str: str) -> Optional[ulid.ULID]:
    """Parse ULID from string"""
    try:
        return ulid.from_str(ulid_str)
    except ValueError:
        return None
