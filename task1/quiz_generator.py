# quiz_generator.py
# Tutorial-Based Hybrid Quiz Generator - 6-Step Progress Bar Support

import re
import google.generativeai as genai
import openai
from typing import List, Dict, Any, Callable, Optional

class QuizGenerator:
    def __init__(self, group2_keys: List[str], nvidia_key: str, group1_keys: List[str]):
        self.group2_keys = group2_keys
        self.nvidia_key = nvidia_key
        self.group1_keys = group1_keys

    def reset(self):
        pass

    def detect_questions(self, text: str) -> List[Dict[str, Any]]:
        questions = []
        patterns = [
            r'(Question \d+[:\s]*)(.+?)(?=\nQuestion \d+|\n\n|$)',
            r'(\(a\)\s*)(.+?)(?=\(b\)|\(c\)|\n\n|$)',
            r'(\([bi]\)\s*)(.+?)(?=\([bi]\)|\n\n|$)',
            r'(Sketch|Calculate|Determine|Find the first|Determine whether)(.+?)(?=\n\n|$)',
        ]

        for pattern in patterns:
            matches = re.finditer(pattern, text, re.DOTALL | re.IGNORECASE)
            for match in matches:
                q_text = (match.group(2) if len(match.groups()) > 1 else match.group(1)).strip()
                if len(q_text) > 20:
                    q_type = self._detect_question_type(q_text)
                    context_start = max(0, match.start() - 80)
                    context = text[context_start:match.end() + 80]
                    questions.append({"original": q_text, "type": q_type, "context": context})

        seen = set()
        unique = []
        for q in questions:
            key = q["original"][:60]
            if key not in seen:
                seen.add(key)
                unique.append(q)
        return unique[:7]

    def _detect_question_type(self, q_text: str) -> str:
        lower = q_text.lower()
        if any(k in lower for k in ["sketch", "draw", "plot"]):
            return "sketch"
        elif any(k in lower for k in ["calculate", "determine", "find the first", "energy", "power"]):
            return "calculation"
        elif any(k in lower for k in ["(a)", "(b)", "(i)", "(ii)"]):
            return "multi_part"
        elif any(k in lower for k in ["choose", "which of the following", "option"]):
            return "mcq"
        elif any(k in lower for k in ["true or false", "t/f"]):
            return "tf"
        return "short"

    def generate_questions(self, text: str, num_questions: int = 6,
                           progress_callback: Optional[Callable] = None) -> List[Dict[str, Any]]:
        if not text or len(text.strip()) < 100:
            return [{"question": "Not enough content.", "answer": "", "type": "short", "explanation": ""}]

        if progress_callback:
            progress_callback("Starting quiz generation", 0)

        original_questions = self.detect_questions(text)

        if progress_callback:
            progress_callback("Detecting original questions", 20)

        content = ""
        for i, q in enumerate(original_questions[:num_questions], 1):
            content += f"\nOriginal Q{i} ({q['type']}):\n{q['original']}\n"

        if progress_callback:
            progress_callback("Preparing prompt and sending to AI", 40)

        prompt = f"""
You are a university lecturer creating new practice questions for students.

Here are the original questions from the assignment/tutorial:

{content}

For each original question:
- Create ONE new similar question (change numbers or examples slightly but keep the same concept and difficulty).
- Keep the same type and structure.
- **You MUST provide the complete correct answer with all calculation steps** — act as the lecturer who is marking the paper.
- Write the answer exactly as you would expect a good student to write it (show all steps clearly).
- Never skip the Answer section.

Format exactly:
Q1 (type): [full new question]
Answer: [detailed answer with steps]
Explanation: [short key point]

End with a "Key Revision Tips" section.
"""

        polished = None

        # Gemini primary
        for key in self.group2_keys:
            try:
                genai.configure(api_key=key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                response = model.generate_content(prompt)
                polished = response.text.strip()
                if polished and len(polished) > 150:
                    break
            except:
                continue

        if not polished and progress_callback:
            progress_callback("Gemini failed → trying NIM fallback", 50)

        # NIM fallback
        if not polished:
            try:
                client = openai.OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=self.nvidia_key)
                response = client.chat.completions.create(
                    model="meta/llama-3.1-70b-instruct",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=2200
                )
                polished = response.choices[0].message.content.strip()
            except:
                polished = None

        if not polished:
            if progress_callback:
                progress_callback("AI failed → using local fallback", 70)
            return [{"question": f"Placeholder Q{i+1}", "answer": "N/A", "type": "short", "explanation": ""} for i in range(num_questions)]

        if progress_callback:
            progress_callback("Formatting the quiz output", 80)

        questions = self._parse_and_clean_llm_output(polished, num_questions)

        if progress_callback:
            progress_callback("Quiz generation complete", 99)

        return questions

    def _parse_and_clean_llm_output(self, text: str, target_num: int) -> List[Dict[str, Any]]:
        questions = []
        lines = text.split("\n")
        current = {}
        for line in lines:
            line = line.strip()
            if line.startswith("Q") and "(" in line and ":" in line:
                if current:
                    questions.append(current)
                typ = line.split("(", 1)[-1].split(")")[0]
                q = line.split(":", 1)[-1].strip()
                current = {"question": q, "type": typ, "answer": "", "explanation": ""}
            elif line.startswith("Answer:"):
                current["answer"] = line.replace("Answer:", "").strip()
            elif line.startswith("Explanation:"):
                current["explanation"] = line.replace("Explanation:", "").strip()
        if current:
            questions.append(current)

        while len(questions) < target_num:
            questions.append({"question": f"Additional practice question {len(questions)+1}", "type": "short", "answer": "N/A", "explanation": ""})
        return questions[:target_num]

    def generate_quiz(self, questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {"questions": questions, "score": 0, "total": len(questions)}# quiz_generator.py
# Tutorial-Based Hybrid Quiz Generator - Brute-force 6-step progress bar via callback

import re
import google.generativeai as genai
import openai
from typing import List, Dict, Any, Callable, Optional

class QuizGenerator:
    def __init__(self, group2_keys: List[str], nvidia_key: str, group1_keys: List[str]):
        self.group2_keys = group2_keys
        self.nvidia_key = nvidia_key
        self.group1_keys = group1_keys

    def reset(self):
        pass

    def detect_questions(self, text: str) -> List[Dict[str, Any]]:
        questions = []
        patterns = [
            r'(Question \d+[:\s]*)(.+?)(?=\nQuestion \d+|\n\n|$)',
            r'(\(a\)\s*)(.+?)(?=\(b\)|\(c\)|\n\n|$)',
            r'(\([bi]\)\s*)(.+?)(?=\([bi]\)|\n\n|$)',
            r'(Sketch|Calculate|Determine|Find the first|Determine whether)(.+?)(?=\n\n|$)',
        ]

        for pattern in patterns:
            matches = re.finditer(pattern, text, re.DOTALL | re.IGNORECASE)
            for match in matches:
                q_text = (match.group(2) if len(match.groups()) > 1 else match.group(1)).strip()
                if len(q_text) > 20:
                    q_type = self._detect_question_type(q_text)
                    context_start = max(0, match.start() - 80)
                    context = text[context_start:match.end() + 80]
                    questions.append({"original": q_text, "type": q_type, "context": context})

        seen = set()
        unique = []
        for q in questions:
            key = q["original"][:60]
            if key not in seen:
                seen.add(key)
                unique.append(q)
        return unique[:7]

    def _detect_question_type(self, q_text: str) -> str:
        lower = q_text.lower()
        if any(k in lower for k in ["sketch", "draw", "plot"]):
            return "sketch"
        elif any(k in lower for k in ["calculate", "determine", "find the first", "energy", "power"]):
            return "calculation"
        elif any(k in lower for k in ["(a)", "(b)", "(i)", "(ii)"]):
            return "multi_part"
        elif any(k in lower for k in ["choose", "which of the following", "option"]):
            return "mcq"
        elif any(k in lower for k in ["true or false", "t/f"]):
            return "tf"
        return "short"

    def generate_questions(self, text: str, num_questions: int = 6,
                           progress_callback: Optional[Callable] = None) -> List[Dict[str, Any]]:
        if not text or len(text.strip()) < 100:
            return [{"question": "Not enough content.", "answer": "", "type": "short", "explanation": ""}]

        if progress_callback:
            progress_callback("Starting quiz generation", 0)

        original_questions = self.detect_questions(text)

        if progress_callback:
            progress_callback("Detecting original questions", 20)

        content = ""
        for i, q in enumerate(original_questions[:num_questions], 1):
            content += f"\nOriginal Q{i} ({q['type']}):\n{q['original']}\n"

        if progress_callback:
            progress_callback("Preparing prompt and sending to AI", 40)

        prompt = f"""
You are a university lecturer creating new practice questions for students.

Here are the original questions from the assignment/tutorial:

{content}

For each original question:
- Create ONE new similar question (change numbers or examples slightly but keep the same concept and difficulty).
- Keep the same type and structure.
- **You MUST provide the complete correct answer with all calculation steps** — act as the lecturer who is marking the paper.
- Write the answer exactly as you would expect a good student to write it (show all steps clearly).
- Never skip the Answer section.

Format exactly:
Q1 (type): [full new question]
Answer: [detailed answer with steps]
Explanation: [short key point]

End with a "Key Revision Tips" section.
"""

        polished = None

        # Gemini primary
        for key in self.group2_keys:
            try:
                genai.configure(api_key=key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                response = model.generate_content(prompt)
                polished = response.text.strip()
                if polished and len(polished) > 150:
                    break
            except:
                continue

        if not polished and progress_callback:
            progress_callback("Gemini failed → trying NIM fallback", 60)

        # NIM fallback
        if not polished:
            try:
                client = openai.OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=self.nvidia_key)
                response = client.chat.completions.create(
                    model="meta/llama-3.1-70b-instruct",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=2200
                )
                polished = response.choices[0].message.content.strip()
            except:
                polished = None

        if not polished:
            if progress_callback:
                progress_callback("AI failed → using local fallback", 80)
            return [{"question": f"Placeholder Q{i+1}", "answer": "N/A", "type": "short", "explanation": ""} for i in range(num_questions)]

        if progress_callback:
            progress_callback("Formatting the quiz output", 90)

        questions = self._parse_and_clean_llm_output(polished, num_questions)

        if progress_callback:
            progress_callback("Quiz generation complete", 99)

        return questions

    def _parse_and_clean_llm_output(self, text: str, target_num: int) -> List[Dict[str, Any]]:
        questions = []
        lines = text.split("\n")
        current = {}
        for line in lines:
            line = line.strip()
            if line.startswith("Q") and "(" in line and ":" in line:
                if current:
                    questions.append(current)
                typ = line.split("(", 1)[-1].split(")")[0]
                q = line.split(":", 1)[-1].strip()
                current = {"question": q, "type": typ, "answer": "", "explanation": ""}
            elif line.startswith("Answer:"):
                current["answer"] = line.replace("Answer:", "").strip()
            elif line.startswith("Explanation:"):
                current["explanation"] = line.replace("Explanation:", "").strip()
        if current:
            questions.append(current)

        while len(questions) < target_num:
            questions.append({"question": f"Additional practice question {len(questions)+1}", "type": "short", "answer": "N/A", "explanation": ""})
        return questions[:target_num]

    def generate_quiz(self, questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {"questions": questions, "score": 0, "total": len(questions)}  
