"""
gui.py
Tkinter-based graphical user interface for the Study Notes Processor.
Uses composition to interact with repository, summarizer, and search engine.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from storage.repository import CourseRepository
from processing.summarizer import ExtractiveSummarizer


class StudyAssistantGUI:
    """
    Main GUI class using Tkinter.
    Composition: owns repository and summarizer instances.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.repo = CourseRepository()
        self.summarizer = ExtractiveSummarizer()

        self._setup_ui()

    def _setup_ui(self):
        """Build the main window layout."""

        # Title
        tk.Label(self.root, text="Study Notes Processor", font=("Arial", 16, "bold")).pack(pady=10)

        # Notebook (tabs)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Tab 1: Add Note
        self._create_add_note_tab(notebook)

        # Tab 2: View / Summarize
        self._create_summarize_tab(notebook)

        # Tab 3: Search
        self._create_search_tab(notebook)

        # Tab 4: Quiz (placeholder)
        self._create_quiz_tab(notebook)

    def _create_add_note_tab(self, notebook):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Add Note")

        tk.Label(tab, text="Course Code:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.course_entry = tk.Entry(tab, width=40)
        self.course_entry.grid(row=0, column=1, pady=5)

        tk.Label(tab, text="Title:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.title_entry = tk.Entry(tab, width=40)
        self.title_entry.grid(row=1, column=1, pady=5)

        tk.Label(tab, text="Content:").grid(row=2, column=0, sticky="nw", padx=5, pady=5)
        self.content_text = scrolledtext.ScrolledText(tab, width=60, height=15)
        self.content_text.grid(row=2, column=1, pady=5)

        tk.Button(tab, text="Save Note", command=self._save_note).grid(row=3, column=1, pady=10, sticky="e")

    def _save_note(self):
        """Stub: save note to repository."""
        course = self.course_entry.get().strip()
        title = self.title_entry.get().strip()
        content = self.content_text.get("1.0", tk.END).strip()

        if not course or not title or not content:
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        # Later: create LectureNote or TutorialNote
        messagebox.showinfo("Success", "Note saved (stub).")
        # self.repo.save_note(note)

    def _create_summarize_tab(self, notebook):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Summarize")

        tk.Label(tab, text="Select note or paste text (stub)").pack(pady=10)
        # Later: dropdown for notes + text area + summarize button

    def _create_search_tab(self, notebook):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Search")

        tk.Label(tab, text="Search query:").pack(pady=5)
        self.search_entry = tk.Entry(tab, width=50)
        self.search_entry.pack(pady=5)

        tk.Button(tab, text="Search", command=self._perform_search).pack(pady=5)

        self.search_result = scrolledtext.ScrolledText(tab, width=80, height=15)
        self.search_result.pack(pady=10)

    def _perform_search(self):
        query = self.search_entry.get().strip()
        self.search_result.delete("1.0", tk.END)
        self.search_result.insert(tk.END, f"Search for '{query}' (stub result)\n")

    def _create_quiz_tab(self, notebook):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Quiz Mode")
        tk.Label(tab, text="Quiz mode - to be implemented").pack(pady=50)