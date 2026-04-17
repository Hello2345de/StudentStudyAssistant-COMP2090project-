# Study Notes Processor

**Turn lengthy lecture notes into clean summaries and practice quizzes**

A simple, exportable desktop app built with Flet that helps students process `.txt` or `.pdf` lecture notes.

- Extracts text + embedded images from PDFs  
- Produces well-structured, exam-ready summaries with bold headings and bullet points  
- Generates 6 high-quality practice questions that match the original style (calculation, sketch, short-answer, etc.) with full step-by-step answers  

## .EXE direct execute (Windows only)
download the .exe file within this folder, and execute it on a windows computer
link to the .exe:
https://drive.google.com/file/d/1ZSXulqw6Bjys3lelW8l77asUWsk5lYFO/view?usp=drive_link

## Module Installation (PyCharm method)

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

## Alternatively enter this command in the terminal:

`python -m pip install pymupdf google-generativeai openai sumy rake-nltk nltk`
 
then enter:
`python -m nltk.downloader punkt punkt_tab stopwords`

## How to Run

  Place these files in the same folder:
-  main.py
-   summarizer.py
-   image_analyzer.py
-   quiz_generator.py
-   config.py

Right-click main.py → Run 'main'.

*or directly execute the .exe file 

The app opens with a main menu for you to choosse between Summarizer or Quiz Generator .

## How to generate output

   1. Click on Summarizer or Quiz Generator
   2. Click Upload File → select .txt or .pdf.
   The raw extracted text appears in the big box (images will be summarized/described by LLM and fuse with the extracted text).

2. Click Generate Summary or Generate Quiz (6 questions).
   Wait for the process to be finished(might take a few minutes for the LLM to return the output)
   output will appear below with formatted structure.
