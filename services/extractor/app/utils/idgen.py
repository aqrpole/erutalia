# services/extractor/app/utils/idgen.py
"""
UUID generation utilities (Qdrant-compatible)
New one has hyphens which are mandated not ULID
"""

import uuid
from typing import Optional

def generate_id() -> str:
    """Generate a Qdrant-compatible unique UUID string"""
    return str(uuid.uuid4())


def generate_id_bytes() -> bytes:
    """Generate UUID as bytes"""
    return uuid.uuid4().bytes


def parse_id(id_str: str) -> Optional[uuid.UUID]:
    """Parse UUID from string, return None if invalid"""
    try:
        return uuid.UUID(id_str)
    except ValueError:
        return None

