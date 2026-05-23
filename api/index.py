from flask import Flask, request, jsonify
import wikipediaapi

app = Flask(__name__)

# Core Setup hidden behind custom agent schemas
wiki = wikipediaapi.Wikipedia(
    user_agent="XtremeAI/3.0 (contact@xtreme_it_solution.com)",
    language="bn",
    extract_format=wikipediaapi.ExtractFormat.WIKI
)

@app.route('/api/analyze', methods=['POST'])
def analyze_data():
    data = request.get_json()
    topic = data.get('topic', '').strip()
    keyword = data.get('keyword', '').strip()

    if not topic or not keyword:
        return jsonify({"status": "error", "message": "টপিক এবং কিউওয়ার্ড দুটিই দেওয়া আবশ্যক।"})

    page = wiki.page(topic)
    
    if not page.exists():
        return jsonify({
            "status": "not_found", 
            "message": f"❌ [Xtreme AI]: আমাদের কোর ডেটাবেসে '{topic}' সংক্রান্ত কোনো ডেটা খুঁজে পাওয়া যায়নি।"
        })
    
    text_lines = page.text.split('\n')
    relevant_sentences = []
    
    for line in text_lines:
        if keyword.lower() in line.lower():
            relevant_sentences.append(line)
            
    if relevant_sentences:
        return jsonify({
            "status": "success",
            "title": f"🎯 '{keyword}' সম্পর্কিত নিখুঁত তথ্য ফিল্টার করা হয়েছে:",
            "content": "\n\n".join(relevant_sentences[:3])
        })
    else:
        return jsonify({
            "status": "summary",
            "title": f"⚠️ '{keyword}' সরাসরি পাওয়া যায়নি। মূল কোর ডেসক্রিপশন:",
            "content": page.summary[:600]
        })

# Vercel needs this wrapper
def handler(environ, start_response):
    return app(environ, start_response)
