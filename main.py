import urllib.request
import urllib.parse
import json
import webbrowser
import re
from sympy import sympify, solve

# --- ভাষা শনাক্তকরণ লজিক ---
def detect_language(text):
    """বাংলা বর্ণমালা থাকলে 'bn' নয়তো 'en' রিটার্ন করবে"""
    if re.search(r'[\u0980-\u09FF]', text):
        return "bn"
    return "en"

# --- উইকিপিডিয়া সার্চ সিস্টেম (All Language Support) ---
def get_wiki_info(query):
    try:
        # অপ্রয়োজনীয় শব্দ (Stop words) ফিল্টার করা
        clean_query = re.sub(r'\b(who is|what is|about|কে|কি|সম্পর্কে|বলতো|তথ্য|give me information about)\b', '', query, flags=re.IGNORECASE).strip()
        
        lang = detect_language(clean_query)
        encoded_query = urllib.parse.quote(clean_query)
        
        # ১. ওপেন সার্চ দিয়ে সঠিক টাইটেল খুঁজে বের করা
        search_url = f"https://{lang}.wikipedia.org/w/api.php?action=opensearch&search={encoded_query}&limit=1&format=json"
        headers = {'User-Agent': 'XtremeAI/5.0 (Education Project)'}
        
        req = urllib.request.Request(search_url, headers=headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
            if len(data) > 1 and data[1]:
                title = data[1][0]
                link = data[3][0]
                
                # ২. সামারি এপিআই থেকে বিস্তারিত তথ্য আনা
                summary_url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title.replace(' ', '_'))}"
                req_s = urllib.request.Request(summary_url, headers=headers)
                
                with urllib.request.urlopen(req_s) as res_s:
                    info = json.loads(res_s.read().decode())
                    extract = info.get('extract', 'বিস্তারিত তথ্য পাওয়া যায়নি।')
                    return {"text": f"🔍 বিষয়: {title}\n📌 তথ্য: {extract}", "url": link}
            else:
                # যদি বাংলায় না পাওয়া যায় তবে ইংরেজিতে ট্রাই করা
                if lang == "bn":
                    return get_wiki_info_en_fallback(clean_query)
                return {"text": "❌ দুঃখিত, এই বিষয়ে কোনো তথ্য আমার ডেটাবেজে নেই।", "url": None}
    except:
        return {"text": "⚠️ নেটওয়ার্ক বা উইকিপিডিয়া সার্ভারে সমস্যা হচ্ছে।", "url": None}

def get_wiki_info_en_fallback(clean_query):
    """বাংলায় তথ্য না থাকলে ইংরেজি উইকিপিডিয়া থেকে নিয়ে আসা"""
    try:
        encoded_query = urllib.parse.quote(clean_query)
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded_query}"
        headers = {'User-Agent': 'XtremeAI/5.0'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode())
            if data.get('type') == 'standard':
                return {"text": f"🔍 বিষয়: {data.get('title')}\n📌 তথ্য (EN): {data.get('extract')}", "url": data.get('content_urls', {}).get('desktop', {}).get('page')}
        return {"text": "❌ কোনো ভাষাতেই তথ্য পাওয়া যায়নি।", "url": None}
    except:
        return {"text": "❌ তথ্য খুঁজে পাওয়া যায়নি।", "url": None}

# --- অ্যাডভান্সড ম্যাথ ও লজিক সলভার ---
def solve_math_pro(query):
    try:
        # আয়-ব্যয় এবং লাভ-ক্ষতি লজিক
        if any(word in query for word in ["লাভ", "ক্ষতি", "আয়", "ব্যয়", "profit", "loss", "income", "expense"]):
            numbers = re.findall(r'\d+', query)
            if len(numbers) >= 2:
                v1, v2 = int(numbers[0]), int(numbers[1])
                res = v1 - v2
                status = "লাভ/উদ্বৃত্ত" if res > 0 else "ক্ষতি/ঘাটতি"
                return f"💰 হিসাব সম্পন্ন: আপনার {status} হয়েছে {abs(res)} টাকা।"

        # Sympy দিয়ে গাণিতিক সমীকরণ সমাধান
        math_symbols = ['+', '-', '*', '/', '^', '(', ')', '=']
        if any(char in query for char in math_symbols) or query.isdigit():
            if '=' in query:
                parts = query.split('=')
                eq = sympify(parts[0].strip() + "-(" + parts[1].strip() + ")")
                sol = solve(eq)
                return f"🔢 সমীকরণের সমাধান: {sol}"
            else:
                result = sympify(query)
                return f"🔢 গাণিতিক ফলাফল: {result}"
    except:
        return None
    return None

# --- মেইন প্রোগ্রাম লুপ ---
def main():
    print("\n" + "═"*45)
    print("      🚀 XTREME AI - UPGRADED PRO EDITION")
    print("      STATUS: Online | MODE: Global Chat")
    print("═"*45)
    print("বন্ধ করতে 'exit' লিখুন।")
    
    while True:
        user_input = input("\n👤 আপনি: ").strip()
        
        if user_input.lower() in ['exit', 'quit', 'বন্ধ']:
            print("🤖 Xtreme AI: বিদায়! ভালো থাকবেন।")
            break
            
        if not user_input:
            print("🤖 Xtreme AI: আপনি আমার কাছে কী জানতে চান? উইকিপিডিয়া প্রশ্ন অথবা ম্যাথ প্রবলেম এখানে লিখুন।")
            continue
            
        # ১. গ্রিটিং চেক
        if user_input.lower() in ["hi", "hello", "হাই", "হ্যালো", "hey"]:
            print("🤖 Xtreme AI: হ্যালো! আমি আপনার স্মার্ট অ্যাসিস্ট্যান্ট। আমি এখন গ্লোবাল উইকিপিডিয়া এবং অ্যাডভান্সড ম্যাথ সাপোর্ট করি। কী সাহায্য লাগবে?")
            continue

        # ২. ম্যাথ প্রসেসিং
        math_res = solve_math_pro(user_input)
        if math_res:
            print(f"🤖 Xtreme AI: {math_res}")
            continue
            
        # ৩. গ্লোবাল উইকিপিডিয়া সার্চ
        print("⌛ তথ্য বিশ্লেষণ করা হচ্ছে...")
        result = get_wiki_info(user_input)
        print(f"\n🤖 Xtreme AI:\n{result['text']}")
        
        if result.get('url'):
            open_link = input("\n🔗 আপনি কি পুরো বিষয়টি ব্রাউজারে দেখতে চান? (y/n): ").lower()
            if open_link == 'y':
                webbrowser.open(result['url'])

if __name__ == "__main__":
    main()
