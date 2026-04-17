"""
processing/image_analyzer.py
Multi-API parallel Gemini vision analyzer with strong Python cleaning
"""

import fitz  # PyMuPDF
from typing import List, Dict, Any
import google.generativeai as genai
from pathlib import Path
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


class ImageAnalyzer:
    def __init__(self, api_keys: List[str]):
        if not api_keys:
            raise ValueError("At least one Gemini API key is required")

        # Use only the first 3 keys for summarizer/image analysis
        self.api_keys = api_keys[:3]
        self.models = []

        for i, key in enumerate(self.api_keys):
            try:
                genai.configure(api_key=key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                self.models.append(model)
                print(f"✅ Summarizer API key {i + 1} loaded")
            except Exception as e:
                print(f"⚠️ Failed to load summarizer API key {i + 1}: {e}")

        if not self.models:
            raise ValueError("No valid summarizer API keys could be loaded")

    def extract_images_and_text(self, pdf_path: str) -> Dict[str, Any]:
        doc = fitz.open(pdf_path)
        full_text = ""
        images = []

        try:
            for page_num, page in enumerate(doc, start=1):
                full_text += page.get_text("text") + "\n\n"
                image_list = page.get_images(full=True)
                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    if base_image:
                        images.append({
                            "bytes": base_image["image"],
                            "page": page_num,
                            "index": img_index
                        })
            return {
                "text": full_text.strip(),
                "images": images,
                "total_pages": len(doc),
                "total_images": len(images)
            }
        finally:
            doc.close()

    def describe_image(self, image_bytes: bytes, page_num: int, model_index: int) -> str:
        prompt = """
You are a helpful study assistant. Describe this lecture note image in 1-2 short sentences.
Focus on: type of visual (graph/chart/diagram), main trend/insight, and exam takeaway.
Keep it concise and natural.
"""
        try:
            response = self.models[model_index].generate_content([
                prompt,
                {"mime_type": "image/jpeg", "data": image_bytes}
            ])
            return f"[Page {page_num}] {response.text.strip()}"
        except Exception as e:
            return f"[Page {page_num}] (Image analysis failed: {str(e)[:80]})"

    def clean_summary(self, raw_text: str) -> str:
        """Strong pure-Python cleaning - forces readable formatting."""
        if not raw_text:
            return raw_text

        # Split and clean line by line
        lines = raw_text.split('\n')
        cleaned = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Force new paragraph after every sentence
            if '. ' in line and not line.startswith(('-', '•', '*')):
                line = line.replace('. ', '.\n\n')

            # Make sure bullet points have spacing before them
            if line.startswith(('-', '•', '*')):
                cleaned.append('\n' + line)
            else:
                cleaned.append(line)

        result = '\n'.join(cleaned)

        # Extra spacing before "Key Takeaways"
        result = result.replace("Key Takeaways", "\n\n**Key Takeaways**")

        return result

    def fuse_summary(self, text_summary: str, image_descriptions: List[str]) -> str:
        """Returns raw text only. Cleaning is done later in Python."""
        if not image_descriptions:
            return text_summary

        combined_input = f"""
Text Summary:
{text_summary}

Image Insights:
{"\n".join(image_descriptions)}

Create a clean study summary.
- Start with 1-2 sentence overall summary
- Use bullet points for key points and graph insights
- Use **bold** for important terms
- End with "Key Takeaways" if useful
"""

        try:
            response = self.models[0].generate_content(combined_input)
            return response.text.strip()
        except Exception as e:
            print(f"Fusion failed: {e}")
            return text_summary + "\n\n[Image fusion issue - using text summary only]"

    def process_pdf(self, pdf_path: str) -> Dict[str, Any]:
        print(f"Processing PDF: {Path(pdf_path).name} ...")
        data = self.extract_images_and_text(pdf_path)

        print(f"Extracted {data['total_pages']} pages and {data['total_images']} images.")

        if not data["images"]:
            return {
                "text": data["text"],
                "image_descriptions": [],
                "images_found": 0
            }

        image_descriptions = []
        with ThreadPoolExecutor(max_workers=len(self.api_keys)) as executor:
            future_to_img = {}
            for i, img in enumerate(data["images"]):
                model_index = i % len(self.api_keys)
                future = executor.submit(self.describe_image, img["bytes"], img["page"], model_index)
                future_to_img[future] = i

            print(f"🚀 Starting parallel analysis of {len(data['images'])} images using {len(self.api_keys)} APIs...")

            for future in as_completed(future_to_img):
                desc = future.result()
                image_descriptions.append(desc)
                print(f"  → Finished image {future_to_img[future] + 1}")

        return {
            "text": data["text"],
            "image_descriptions": image_descriptions,
            "images_found": len(data["images"])
        }
