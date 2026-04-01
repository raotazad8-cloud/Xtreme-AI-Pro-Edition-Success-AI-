import urllib.request
import urllib.parse
import json
import re
from googletrans import Translator
from sympy import sympify, solve

# ট্রান্সলেটর অবজেক্ট তৈরি
translator = Translator()

def translate_to_english(text):
    """যেকোনো ভাষাকে ইংরেজিতে অনুবাদ করার ফাংশন"""
    try:
        translation = translator.translate(text, dest='en')
        return translation.text
    except:
        return text

def get_wiki_info(query):
    """উইকিপিডিয়া তথ্য এবং অটো-ট্রান্সলেট সিস্টেম"""
    try:
        clean_query = re.sub(r'\b(who is|what is|কে|কি|সম্পর্কে)\b', '', query, flags=re.IGNORECASE).strip()
        
        # বাংলা কি না চেক করা
        lang = "bn" if re.search(r'[\u0980-\u09FF]', clean_query) else "en"
        encoded_query = urllib.parse.quote(clean_query)
        
        # উইকিপিডিয়া থেকে তথ্য আনা
        url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{encoded_query}"
        headers = {'User-Agent': 'XtremeAI/6.0'}
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode())
            original_text = data.get('extract', 'No info found.')
            
            # ব্যবহারকারী যদি ইংরেজিতে উত্তর চায় (ধরা যাক প্রশ্নে 'in english' থাকলে)
            if "english" in query.lower() or "ইংরেজি" in query:
                print("🔠 ইংরেজিতে অনুবাদ করা হচ্ছে...")
                translated_text = translate_to_english(original_text)
                return f"🔍 Subject: {data.get('title')}\n📌 English Info: {translated_text}"
            
            return f"🔍 বিষয়: {data.get('title')}\n📌 তথ্য: {original_text}"
    except:
        return "❌ তথ্য খুঁজে পাওয়া যায়নি।"

def main():
    print("🚀 XTREME AI - TRANSLATION ENABLED")
    
    while True:
        user_input = input("\n👤 আপনি: ").strip()
        if user_input.lower() == 'exit': break
        
        # যদি ইউজার বলে "Translate: [লেখা]"
        if user_input.lower().startswith("translate:"):
            text_to_convert = user_input.split(":", 1)[1]
            result = translate_to_english(text_to_convert)
            print(f"🤖 Xtreme AI (Translated): {result}")
            continue

        # উইকিপিডিয়া চেক
        print("⌛ প্রসেসিং...")
        print(f"🤖 Xtreme AI: {get_wiki_info(user_input)}")

if __name__ == "__main__":
    main()
