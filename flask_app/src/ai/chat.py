import os
from google import genai


API_KEY = os.getenv('GEMINI_API_KEY')
# API_KEY = envs.get('GEMINI_API_KEY')
client = genai.Client(api_key=API_KEY)

while True:
    prompt = input('>>> ')
    if prompt in ('q', 'quit', 'exit', 'bye'):
        break
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    print(response.text)
    # return response.text or ""


# if '__main__' == __name__:
#     prompt = input('Enter your prompt:\n>>> ')
#     print(gemini_generate_content(prompt))
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
