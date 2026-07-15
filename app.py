from fastapi import FastAPI, HTTPException, Body
from google import genai
import uvicorn
import os

# Replace with your own Gemini API key
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
app = FastAPI(
    title="Python Code Explainer API",
    description="Explains Python code line by line using Gemini",
    version="1.0"
)

@app.get("/")
def home():
    return {
        "message": "Python Code Explainer API Running"
    }

@app.post("/explain")
def explain_code(code: str = Body(..., media_type="text/plain")):

    prompt = f"""
You are an expert Python tutor.

Explain the following Python code line by line.

Rules:
1. Explain every line separately.
2. Mention what each variable stores.
3. Explain loops if present.
4. Explain functions if present.
5. Explain conditions if present.
6. Use simple English.
7. Number the explanations according to the code lines.

Python Code:

{code}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return {
            "explanation": response.text
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
