"""
models/note.py
Core data models for notes using OOP concepts.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Any


class NoteEntry(ABC):
    """Abstract base class for all note types."""

    def __init__(self, course_code: str, title: str, content: str):
        self._course_code = course_code
        self._title = title
        self._content = content
        self._created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        self._summary: str = None
        self._questions: List[Dict[str, Any]] = []

    @property
    def course_code(self) -> str:
        return self._course_code

    @property
    def title(self) -> str:
        return self._title

    @property
    def content(self) -> str:
        return self._content

    @abstractmethod
    def get_type(self) -> str:
        pass

    def add_summary(self, summary: str) -> None:
        self._summary = summary

    def add_question(self, question: Dict[str, Any]) -> None:
        self._questions.append(question)


class LectureNote(NoteEntry):
    def get_type(self) -> str:
        return "Lecture"


class TutorialNote(NoteEntry):
    def get_type(self) -> str:
        return "Tutorial"
