from flask import Flask, render_template, request, jsonify
import anthropic
import wikipedia
import os

app = Flask(__name__)

CLAUDE_API_KEY = "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"
client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("msg", "").strip()
    
    if not user_input:
        return jsonify({"reply": "I didn't receive any message."})

    lower_input = user_input.lower()

    if lower_input.startswith("who is") or lower_input.startswith("what is"):
        try:
            query = user_input.replace("Who is", "").replace("who is", "").replace("What is", "").replace("what is", "").replace("?", "").strip()
            wikipedia.set_lang("en") # ইংরেজিতে সার্চ করবে
            summary = wikipedia.summary(query, sentences=3)
            return jsonify({"reply": f"🌍 **Wikipedia says:**\n{summary}"})
        except wikipedia.exceptions.DisambiguationError:
            pass 
        except wikipedia.exceptions.PageError:
            pass 

    
    try:
        response = client.messages.create(
            model="claude-3-opus-20240229", 
            max_tokens=1024,
            messages=[
                {"role": "user", "content": f"Act as Xtreme AI Pro Edition (Recreated). Provide professional IT/Coding help and answer questions nicely. User: {user_input}"}
            ]
        )
        reply = response.content[0].text
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": "🤖 Error: Please check your Anthropic API Key or Connection."})

if __name__ == '__main__':
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
