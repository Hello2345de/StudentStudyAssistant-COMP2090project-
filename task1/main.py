# task1/main.py
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import flet as ft
import asyncio
from summarizer import KeywordFocusedSummarizer
from image_analyzer import ImageAnalyzer
from quiz_generator import QuizGenerator
from config import GEMINI_API_KEYS, NVIDIA_API_KEY

def main(page: ft.Page):
    page.title = "Study Notes Processor"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 30
    page.window_width = 1150
    page.window_height = 820
    page.scroll = ft.ScrollMode.AUTO

    # Backend initialization
    summarizer = KeywordFocusedSummarizer(GEMINI_API_KEYS, NVIDIA_API_KEY)
    image_analyzer = ImageAnalyzer(GEMINI_API_KEYS[:3])
    quiz_generator = QuizGenerator(
        group2_keys=GEMINI_API_KEYS[3:],
        nvidia_key=NVIDIA_API_KEY,
        group1_keys=GEMINI_API_KEYS[:3]
    )

    # Shared loading & status components
    loading_icon = ft.ProgressRing(width=20, height=20, stroke_width=3, visible=False)
    loading_text = ft.Text("", size=15, color=ft.Colors.BLUE_200, visible=False)
    status_text = ft.Text("", size=14, color=ft.Colors.BLUE_200)

    def show_loading(message: str):
        loading_icon.visible = True
        loading_text.visible = True
        loading_text.value = message
        status_text.value = ""
        page.update()

    def hide_loading():
        loading_icon.visible = False
        loading_text.visible = False
        page.update()

    # === FilePicker as Service (fixed version) ===
    file_picker = ft.FilePicker()
    page.services.append(file_picker)

    # ==================== MAIN MENU ====================
    def show_main_menu():
        page.controls.clear()

        menu_view = ft.Column(
            controls=[
                ft.Text("Study Notes Processor", size=38, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Text("Summarize your notes or Generate a quiz", size=18, color=ft.Colors.GREY_400, text_align=ft.TextAlign.CENTER),
                ft.Container(height=50),
                ft.Row(
                    controls=[
                        # Summarizer Card
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Icon(ft.Icons.SUMMARIZE_ROUNDED, size=72, color=ft.Colors.BLUE_400),
                                        ft.Text("Summarizer", size=26, weight=ft.FontWeight.BOLD),
                                        ft.Text(
                                            "Turn lengthy notes into clean and structured summaries",
                                            size=16,
                                            color=ft.Colors.GREY_300,
                                            text_align=ft.TextAlign.CENTER,
                                        ),
                                        ft.Container(height=30),
                                        ft.ElevatedButton(
                                            "Open Summarizer",
                                            icon=ft.Icons.ARROW_FORWARD,
                                            width=260,
                                            height=55,
                                            style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_600),
                                            on_click=lambda e: show_summarizer_page(),
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=16,
                                ),
                                padding=40,
                                width=420,
                                height=380,
                            ),
                            elevation=10,
                        ),
                        # Quiz Generator Card
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Icon(ft.Icons.QUESTION_MARK_ROUNDED, size=72, color=ft.Colors.GREEN_400),
                                        ft.Text("Quiz Generator", size=26, weight=ft.FontWeight.BOLD),
                                        ft.Text(
                                            "Create practice quizzes with examples from your notes",
                                            size=16,
                                            color=ft.Colors.GREY_300,
                                            text_align=ft.TextAlign.CENTER,
                                        ),
                                        ft.Container(height=30),
                                        ft.ElevatedButton(
                                            "Open Quiz Generator",
                                            icon=ft.Icons.ARROW_FORWARD,
                                            width=260,
                                            height=55,
                                            style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_600),
                                            on_click=lambda e: show_quiz_page(),
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=16,
                                ),
                                padding=40,
                                width=420,
                                height=380,
                            ),
                            elevation=10,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=50,
                ),
                ft.Container(height=40),
                ft.Row([loading_icon, loading_text, status_text], alignment=ft.MainAxisAlignment.CENTER, spacing=12),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )

        page.add(menu_view)
        page.update()

    # ==================== SUMMARIZER PAGE ====================
    def show_summarizer_page():
        page.controls.clear()

        input_text = ft.TextField(
            label="Paste your lecture notes here or upload a file",
            multiline=True,
            min_lines=12,
            max_lines=18,
            expand=True,
            border_radius=8,
        )

        output_area = ft.Text(
            "Output will appear here...",
            size=15,
            selectable=True,
            color=ft.Colors.GREY_400,
        )

        def upload_file(e):
            async def pick():
                files = await file_picker.pick_files(
                    allow_multiple=False,
                    allowed_extensions=["txt", "pdf"],
                )
                if not files:
                    return

                file_path = files[0].path
                show_loading("Processing file...")

                try:
                    if file_path.lower().endswith(".pdf"):
                        analysis_result = image_analyzer.process_pdf(file_path)
                        raw_text = analysis_result["text"]
                    else:
                        with open(file_path, "r", encoding="utf-8") as f:
                            raw_text = f.read()

                    input_text.value = raw_text
                    output_area.value = "File loaded successfully.\n\nClick 'Generate Summary' to continue."
                    output_area.color = ft.Colors.GREY_300
                    status_text.value = "✅ File loaded"
                    status_text.color = ft.Colors.GREEN
                except Exception as ex:
                    status_text.value = f"❌ Error: {str(ex)[:100]}"
                    status_text.color = ft.Colors.RED
                finally:
                    hide_loading()
                    page.update()

            page.run_task(pick)

        async def generate_summary(e):
            text = input_text.value.strip()
            if not text:
                output_area.value = "Please provide some content first."
                output_area.color = ft.Colors.RED
                page.update()
                return

            show_loading("Generating summary... (this may take a minute)")
            try:
                summary = await asyncio.to_thread(
                    lambda: summarizer.summarize(text, sentences_count=18)
                )
                output_area.value = summary
                output_area.color = ft.Colors.WHITE
                status_text.value = "✅ Summary generated successfully"
                status_text.color = ft.Colors.GREEN
            except Exception as ex:
                output_area.value = f"Error: {str(ex)}"
                output_area.color = ft.Colors.RED
                status_text.value = "❌ Failed to generate summary"
                status_text.color = ft.Colors.RED
            finally:
                hide_loading()
                page.update()

        # Summarizer UI
        summarizer_view = ft.Column(
            controls=[
                ft.Row([
                    ft.IconButton(icon=ft.Icons.ARROW_BACK, tooltip="Back to Menu", on_click=lambda e: show_main_menu()),
                    ft.Text("Summarizer", size=28, weight=ft.FontWeight.BOLD),
                ]),
                ft.Row([
                    ft.ElevatedButton("Upload .txt or .pdf", icon=ft.Icons.UPLOAD_FILE, on_click=upload_file),
                    ft.ElevatedButton("Generate Summary", icon=ft.Icons.SUMMARIZE, on_click=generate_summary),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(
                    content=input_text,
                    expand=True,
                    padding=10,
                    border=ft.border.all(1, ft.Colors.GREY_500),
                    border_radius=8,
                ),
                ft.Text("Summary Output:", weight=ft.FontWeight.BOLD, size=16),
                ft.Container(
                    content=output_area,
                    expand=True,
                    padding=15,
                    border=ft.border.all(1, ft.Colors.GREY_500),
                    border_radius=8,
                ),
                ft.Row([loading_icon, loading_text, status_text], alignment=ft.MainAxisAlignment.CENTER),
            ],
            spacing=15,
            expand=True,
        )

        page.add(summarizer_view)
        page.update()

    # ==================== QUIZ GENERATOR PAGE (with Upload added) ====================
    def show_quiz_page():
        page.controls.clear()

        input_text = ft.TextField(
            label="Paste your lecture notes here or upload a file",
            multiline=True,
            min_lines=12,
            max_lines=18,
            expand=True,
            border_radius=8,
        )

        output_area = ft.Text(
            "Generated quiz will appear here...",
            size=15,
            selectable=True,
            color=ft.Colors.GREY_400,
        )

        def upload_file(e):
            async def pick():
                files = await file_picker.pick_files(
                    allow_multiple=False,
                    allowed_extensions=["txt", "pdf"],
                )
                if not files:
                    return

                file_path = files[0].path
                show_loading("Processing file...")

                try:
                    if file_path.lower().endswith(".pdf"):
                        analysis_result = image_analyzer.process_pdf(file_path)
                        raw_text = analysis_result["text"]
                    else:
                        with open(file_path, "r", encoding="utf-8") as f:
                            raw_text = f.read()

                    input_text.value = raw_text
                    output_area.value = "File loaded successfully.\n\nClick 'Generate Quiz' to continue."
                    output_area.color = ft.Colors.GREY_300
                    status_text.value = "✅ File loaded"
                    status_text.color = ft.Colors.GREEN
                except Exception as ex:
                    status_text.value = f"❌ Error: {str(ex)[:100]}"
                    status_text.color = ft.Colors.RED
                finally:
                    hide_loading()
                    page.update()

            page.run_task(pick)

        async def generate_quiz(e):
            content = input_text.value.strip()
            if not content or len(content) < 100:
                output_area.value = "Please paste enough content (at least 100 characters) to generate a quiz."
                output_area.color = ft.Colors.RED
                page.update()
                return

            show_loading("Generating quiz... (this may take a few minutes)")
            try:
                questions = await asyncio.to_thread(
                    lambda: quiz_generator.generate_questions(content, num_questions=6)
                )

                quiz_text = "=== Generated Quiz ===\n\n"
                for i, q in enumerate(questions, 1):
                    q_type = q.get('type', 'short')
                    question = q.get('question', 'No question')
                    answer = q.get('answer', 'No answer')
                    quiz_text += f"Q{i} ({q_type}):\n{question}\n\nAnswer: {answer}\n\n{'-'*50}\n\n"

                output_area.value = quiz_text
                output_area.color = ft.Colors.WHITE
                status_text.value = f"✅ Quiz generated successfully ({len(questions)} questions)"
                status_text.color = ft.Colors.GREEN
            except Exception as ex:
                output_area.value = f"Quiz generation failed: {str(ex)}"
                output_area.color = ft.Colors.RED
                status_text.value = "❌ Quiz generation failed"
                status_text.color = ft.Colors.RED
            finally:
                hide_loading()
                page.update()

        quiz_view = ft.Column(
            controls=[
                ft.Row([
                    ft.IconButton(icon=ft.Icons.ARROW_BACK, tooltip="Back to Menu", on_click=lambda e: show_main_menu()),
                    ft.Text("Quiz Generator", size=28, weight=ft.FontWeight.BOLD),
                ]),
                ft.Row([
                    ft.ElevatedButton("Upload .txt or .pdf", icon=ft.Icons.UPLOAD_FILE, on_click=upload_file),
                    ft.ElevatedButton("Generate Quiz (6 questions)", icon=ft.Icons.QUESTION_ANSWER, on_click=generate_quiz),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(
                    content=input_text,
                    expand=True,
                    padding=10,
                    border=ft.border.all(1, ft.Colors.GREY_500),
                    border_radius=8,
                ),
                ft.Text("Quiz Output:", weight=ft.FontWeight.BOLD, size=16),
                ft.Container(
                    content=output_area,
                    expand=True,
                    padding=15,
                    border=ft.border.all(1, ft.Colors.GREY_500),
                    border_radius=8,
                ),
                ft.Row([loading_icon, loading_text, status_text], alignment=ft.MainAxisAlignment.CENTER),
            ],
            spacing=15,
            expand=True,
        )

        page.add(quiz_view)
        page.update()

    # Start the app with Main Menu
    show_main_menu()


ft.app(target=main)
