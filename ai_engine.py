import os
import time
import random
from dotenv import load_dotenv

try:
    from google import genai
    USING_NEW_SDK = True
except ImportError:
    import google.generativeai as genai
    USING_NEW_SDK = False

load_dotenv()

CANDIDATE_MODELS = [
    "gemini-3.7-flash",
    "gemini-3.1-flash-lite",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
]

RETRYABLE = ("503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED", "500", "INTERNAL", "DEADLINE")
SKIP_MODEL = ("404", "NOT_FOUND")


class AIEngine:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            if USING_NEW_SDK:
                self.client = genai.Client(api_key=self.api_key)
            else:
                genai.configure(api_key=self.api_key)
                self.client = True
        else:
            self.client = None

    def generate_inventory_analysis(self, object_counts: dict) -> str:
        if not object_counts:
            return "No objects detected in the image to analyze."

        if not self.api_key or not self.client:
            total_items = sum(object_counts.values())
            breakdown = ", ".join([f"{k}: {v}" for k, v in object_counts.items()])
            return (
                f"**[Offline Mode - API Key Missing]**\n\n"
                f"Total Detected Objects: {total_items}\n"
                f"Category Breakdown: {breakdown}\n\n"
                f"*(Add GEMINI_API_KEY to your .env file to enable Generative AI narrative generation.)*"
            )

        prompt = f"""
You are an expert AI inventory and visual analytics assistant for an automated facility management system called AURA.

Analyze the following object detection counts obtained from a computer vision scan:
{object_counts}

Provide a structured operational report in Markdown format with the following sections:
1. **Visual Scan Summary**: State total count and distinct categories identified.
2. **Operational Insights**: Briefly analyze what this environment or inventory layout represents.
3. **Actionable Recommendations**: Give 1-2 practical storage, safety, or inventory control recommendations based on the detected items.

Keep the response concise, professional, and directly actionable.
"""

        last_error = "unknown error"

        for model_name in CANDIDATE_MODELS:
            delay = 2
            for attempt in range(3):
                try:
                    if USING_NEW_SDK:
                        response = self.client.models.generate_content(
                            model=model_name,
                            contents=prompt,
                        )
                    else:
                        model = genai.GenerativeModel(model_name)
                        response = model.generate_content(prompt)

                    if response and response.text:
                        print(f"[AURA] Gemini model used: {model_name}")
                        return response.text
                    last_error = "empty response"
                    break
                except Exception as e:
                    last_error = str(e)
                    if any(code in last_error for code in SKIP_MODEL):
                        break
                    if any(code in last_error for code in RETRYABLE):
                        if attempt < 2:
                            time.sleep(delay + random.uniform(0, 1))
                            delay *= 2
                            continue
                        break
                    break

        return f"AI Analysis Unavailable: Unable to connect to Gemini API ({last_error}). Object detection data remains intact."
