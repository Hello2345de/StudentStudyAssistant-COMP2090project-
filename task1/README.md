# Study Notes Processor

**Transform messy lecture notes into clean summaries and practice quizzes — instantly.**

A simple, exportable desktop app built with Flet that helps students process `.txt` or `.pdf` lecture notes.

- Extracts text + embedded images from PDFs  
- Produces well-structured, exam-ready summaries with bold headings and bullet points  
- Generates 6 high-quality practice questions that match the original style (calculation, sketch, short-answer, etc.) with full step-by-step answers  

Fully local and shareable — anyone with Python can run it.

---

## 📥 Installation (PyCharm only)

No terminal commands needed.

1. Open your project in **PyCharm**.  
2. Go to **File → Settings → Project → Python Interpreter**.  
3. Click the **+** button and install these packages **one by one**:

   - `flet`
   - `pymupdf`
   - `google-generativeai`
   - `openai`
   - `sumy`
   - `rake-nltk`
   - `nltk`

4. After installing `nltk`, run this **once** in the PyCharm console:

   ```python
   import nltk
   nltk.download(['punkt', 'punkt_tab', 'stopwords'])

🚀 How to Run

Place these files in the same folder:
main.py
summarizer.py
image_analyzer.py
quiz_generator.py
config.py

Right-click main.py → Run 'main'.

The app opens with a clean main menu offering Summarizer and Quiz Generator cards.

📖 How to Use
Step-by-step (works the same for both tools)

Click Summarizer or Quiz Generator card.
Click Upload File → select .txt or .pdf.
The raw extracted text appears in the big box (you can edit it).

Click Generate Summary or Generate Quiz (6 questions).
Wait for the blue loading ring + message:“Generating… This may take a few minutes”
Polished output appears below (formatted with headings, bullets, and clean spacing).
