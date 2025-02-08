import os
from google import genai


def gemini_generate_content(prompt: str) -> str:
    API_KEY = os.getenv('GEMINI_API_KEY')
    client = genai.Client(api_key=API_KEY)

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    return response.text or ""


if '__main__' == __name__:
    prompt = input('Enter your prompt:\n>>> ')
    print(gemini_generate_content(prompt))
'''
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=YOUR_API_KEY" \
-H 'Content-Type: application/json' \
-X POST \
-d '{
  "contents": [{
    "parts":[{"text": "Explain how AI works"}]
    }]
   }'
'''
