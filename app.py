from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import re
import os

app = Flask(__name__)

# --- 🚀 Google Gemini API Key ---
GEN_API_KEY = "AIzaSyBNr7ereYdLx-atWYAlK9i4E5wb0dqQk4g"
genai.configure(api_key=GEN_API_KEY)

# AI Configuration
generation_config = {
  "temperature": 0.7,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("msg", "").strip()
    
    if not user_input:
        return jsonify({"reply": "I didn't receive any message."})

    # ১. ম্যাথ সলভার (দ্রুত সমাধান)
    if re.match(r'^[0-9+\-*/().%^ ]+$', user_input) and re.search(r'\d', user_input):
        try:
            res = str(eval(user_input.replace('^', '**')))
            return jsonify({"reply": f"🔢 Math Result: {res}"})
        except: pass

    # ২. Gemini AI (কোড এবং সাধারণ প্রশ্ন)
    try:
        prompt = f"Act as Xtreme AI Plus for Xtreme IT Solution. Provide professional and clear help. User: {user_input}"
        response = model.generate_content(prompt)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": "🤖 AI Error: Please check connection or API limits."})

if __name__ == '__main__':
    app.run(debug=True)
