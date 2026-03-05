"""
processing/summarizer.py
Handles text summarization.
Future: sumy (LexRank/Edmundson) + nltk.
"""

from abc import ABC, abstractmethod


class Summarizer(ABC):
    """Abstract summarizer."""

    @abstractmethod
    def generate_summary(self, text: str, num_sentences: int = 5) -> str:
        pass


class ExtractiveSummarizer(Summarizer):
    """Concrete stub for extractive summary."""

    def generate_summary(self, text: str, num_sentences: int = 5) -> str:
        # Placeholder - later use Sumy
        return "Summary placeholder: " + text[:200] + "..."
