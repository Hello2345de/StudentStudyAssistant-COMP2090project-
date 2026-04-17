# summarizer.py
# Hybrid KeywordFocusedSummarizer v10 - Fully general-purpose + state reset

import sys
import re
import google.generativeai as genai
import openai
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.edmundson import EdmundsonSummarizer
from sumy.nlp.stemmers import Stemmer
from rake_nltk import Rake
import nltk
from nltk.corpus import stopwords
from typing import List, Dict

nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)


class KeywordFocusedSummarizer:
    def __init__(self, api_keys: List[str], nvidia_api_key: str):
        self.api_keys = api_keys
        self.nvidia_api_key = nvidia_api_key
        self.language = "english"
        self.tokenizer = Tokenizer(self.language)
        self.stemmer = Stemmer(self.language)
        self.stop_words = set(stopwords.words(self.language))
        self.reset()   # ensure clean state at creation

    def reset(self):
        """Clear all cached state so each generation starts fresh"""
        self.last_raw_summary = None
        self.last_structured = None
        self.last_keywords = None

    # ======================
    # LOCAL PRE-PROCESSING (general)
    # ======================
    def get_keywords(self, text: str, top_n: int = 20) -> list:
        r = Rake()
        r.extract_keywords_from_text(text)
        ranked = r.get_ranked_phrases()[:top_n]
        keywords = set()
        for phrase in ranked:
            keywords.update(phrase.lower().split())
        return list(keywords)

    def pre_clean_raw_summary(self, raw_summary: str) -> str:
        raw_summary = re.sub(r'https?://\S+', '', raw_summary)
        raw_summary = re.sub(r'\b\d+\s*$', '', raw_summary, flags=re.MULTILINE)
        raw_summary = re.sub(r'\b(page|ref|textbook)\b.*?\d+', '', raw_summary, flags=re.IGNORECASE)
        raw_summary = re.sub(r'\s+', ' ', raw_summary).strip()
        return raw_summary

    def advanced_split_sentences(self, text: str):
        parts = re.split(r'(?<=[.!?])\s+', text)
        new_parts = []
        for p in parts:
            p = re.sub(r'(\d+\s*)', r'\n\1', p)
            p = re.sub(r'(Example|Step|Note):', r'\n\1:', p, flags=re.IGNORECASE)
            p = re.sub(r'(•|\$|x\[|x\(|t=|\(t\))', r'\n\1', p)
            new_parts.extend([s.strip() for s in p.split('\n') if s.strip()])
        return [s for s in new_parts if len(s) > 10]

    # ======================
    # 2. LOCAL STRUCTURING (now fully general)
    # ======================
    def structure_lecture_summary(self, raw_summary: str) -> Dict[str, List[str]]:
        cleaned = self.pre_clean_raw_summary(raw_summary)
        sentences = self.advanced_split_sentences(cleaned)

        # No hard-coded topics anymore — just collect everything
        sections = {"main_content": sentences, "additional": []}
        return sections

    # ======================
    # 3. LLM POLISH - Gemini primary + NIM fallback
    # ======================
    def llm_polish_summary(self, structured_sections: Dict[str, List[str]], image_descriptions: List[str] = None) -> str:
        if not any(structured_sections.values()):
            return "**No content to summarize.**"

        content = "\n".join(structured_sections["main_content"])
        if structured_sections["additional"]:
            content += "\nAdditional Concepts:\n" + "\n".join(structured_sections["additional"])

        if image_descriptions:
            content += "\nImage Insights:\n" + "\n".join(image_descriptions)

        prompt = f"""
You are a university lecturer creating clean, exam-ready study notes for any subject.

Here is the cleaned lecture content:

{content}

Organize it into professional student notes:
- Detect the natural main topics from the content itself.
- Use clear bold headings for each major topic.
- One clear bullet per key idea.
- Use sub-bullets where helpful.
- Keep language simple, short, and easy to understand.
- Bold important terms.
- Remove any fragments or repetition.
- End with a short Key Takeaways section.

Return only the formatted notes.
"""

        # 1. Gemini primary
        for key in self.api_keys:
            try:
                genai.configure(api_key=key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                response = model.generate_content(prompt)
                polished = response.text.strip()
                if polished and len(polished) > 100:
                    return polished
            except Exception as e:
                print(f"Gemini key failed: {e}")
                continue

        # 2. NVIDIA NIM fallback
        try:
            client = openai.OpenAI(
                base_url="https://integrate.api.nvidia.com/v1",
                api_key=self.nvidia_api_key
            )
            response = client.chat.completions.create(
                model="meta/llama-3.1-70b-instruct",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=2000
            )
            polished = response.choices[0].message.content.strip()
            if polished and len(polished) > 100:
                return polished
        except Exception as e:
            print(f"NVIDIA NIM fallback failed: {e}")

        # 3. Local fallback
        return self.local_fallback(structured_sections)

    def local_fallback(self, structured_sections: Dict[str, List[str]]) -> str:
        lines = ["**Lecture Summary**", ""]
        for b in structured_sections["main_content"]:
            lines.append(f"• {b}")
        if structured_sections["additional"]:
            lines.append("")
            lines.append("**Additional Concepts**")
            for b in structured_sections["additional"]:
                lines.append(f"• {b}")
        return "\n".join(lines)

    # ======================
    # MAIN ENTRY POINT
    # ======================
    def summarize(self, text: str, sentences_count: int = 18, image_descriptions: List[str] = None) -> str:
        if not text or not text.strip():
            return "**No text provided for summarization.**"

        self.reset()   # ← Clear all previous state

        try:
            bonus_words = self.get_keywords(text)
            parser = PlaintextParser.from_string(text, self.tokenizer)
            summarizer = EdmundsonSummarizer(self.stemmer)
            summarizer.null_words = self.stop_words
            summarizer.stigma_words = {"however", "therefore", "moreover", "furthermore", "additionally",
                                       "in conclusion", "finally", "thus"}
            if bonus_words:
                summarizer.bonus_words = set(bonus_words)

            summary_sentences = summarizer(parser.document, sentences_count)
            raw_summary = " ".join(str(s) for s in summary_sentences)

            structured = self.structure_lecture_summary(raw_summary)

            final_summary = self.llm_polish_summary(structured, image_descriptions)
            return final_summary

        except Exception as ex:
            print(f"Error in summarizer: {ex}")
            return f"**Error generating summary:** {str(ex)}"
