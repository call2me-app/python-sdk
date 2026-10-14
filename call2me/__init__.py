"""Call2Me Python SDK — Build AI voice agents in minutes."""

from .client import Call2Me, Call2MeError
# `__all__` bunları ilan ediyordu ama import edilmiyorlardı:
# `from call2me import Agent` → ImportError (PyPI 1.4.0'da da vardı).
from .models import Agent, Call, KnowledgeBase

__version__ = "1.5.2"
__all__ = ["Call2Me", "Call2MeError", "Agent", "Call", "KnowledgeBase"]
