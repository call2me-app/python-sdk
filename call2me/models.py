"""Type definitions for Call2Me SDK."""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass
class Agent:
    agent_id: str
    agent_name: str
    voice_id: str
    language: str
    status: str


@dataclass
class Call:
    call_id: str
    agent_id: str
    direction: str
    call_status: str
    duration_ms: Optional[int] = None
    from_number: Optional[str] = None
    to_number: Optional[str] = None


@dataclass
class KnowledgeBase:
    id: str
    name: str
    description: Optional[str] = None
    sources_count: int = 0
