# COMP2090SEF Individual Project - Study Notes Processor & Smart Revision Assistant

**Task 1: OOP-based Application Development**  

## Project Overview (Task 1)

This is a Python GUI application designed to help students process and revise lecture/tutorial notes more effectively.

**Core purpose**:
- Input and organize notes (lecture or tutorial) with metadata (course code, title, date)
- Generate concise **extractive summaries** of the content
- Automatically create basic **practice questions** (short answer, fill-in-the-blank, true/false, etc.)
- Provide a simple graphical interface (Tkinter) for adding, viewing, and interacting with notes

The application solves a real-life problem: students often struggle with scattered notes, manual summarization, and creating self-test questions. This tool offers a structured, private, persistent alternative to pasting notes into external AI every time.

**Current status (pre-submission 8 March 2026)**:
- Basic OOP structure implemented
- Tkinter GUI with tabs for adding notes and placeholders for summarize/quiz
- Persistence, summarization, and question generation stubs ready
- Modular design across 6 .py files

## OOP Concepts Demonstrated (Preliminary)

The project uses **all core OOP concepts** from the course:

- **Abstraction**: `NoteEntry` ABC in `models/note.py`
- **Inheritance**: `LectureNote` and `TutorialNote` inherit from `NoteEntry`
- **Encapsulation**: Protected attributes (`_course_code`, `_content`, etc.) + `@property` getters
- **Polymorphism**: `get_type()` method overridden in subclasses
- **Composition**: `StudyAssistantGUI` owns instances of `CourseRepository`, `Summarizer`, `QuestionGenerator`
- **Modular programming**: Separated into models, storage, processing (summarizer + question generator), gui

Future additions will include dunder methods (`__str__`, `__repr__`), class/static methods, and operator overloading if needed.



