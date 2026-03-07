"""
storage/repository.py
Handles persistence using composition.
"""

import json
from typing import List
from models.note import NoteEntry


class CourseRepository:
    """Manages collection of notes for different courses."""

    def __init__(self, data_file: str = "notes_data.json"):
        self._data_file = data_file
        self._notes: List[NoteEntry] = []
        self._load_notes()

    def _load_notes(self) -> None:
        pass  # Stub: load from JSON

    def save_note(self, note: NoteEntry) -> None:
        self._notes.append(note)
        self._save_to_file()

    def _save_to_file(self) -> None:
        pass  # Stub: serialize to JSON

    def get_notes_by_course(self, course_code: str) -> List[NoteEntry]:
        return [n for n in self._notes if n.course_code == course_code]

    def search_notes(self, keyword: str) -> List[NoteEntry]:
        return []  # Stub: later use search engine
