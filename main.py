import urllib.request
import urllib.parse
import json
import webbrowser
import re
from sympy import sympify, solve

def solve_math_pro(query):
    """sympy এবং রেগুলার এক্সপ্রেশন ব্যবহার করে অংক সমাধান"""
    try:
        # লাভ-ক্ষতি বা আয়-ব্যয় শনাক্ত করা (যেমন: ৫০০ আয় ২০০ ব্যয়)
        if any(word in query for word in ["লাভ", "ক্ষতি", "আয়", "ব্যয়", "profit", "loss", "income"]):
            numbers = re.findall(r'\d+', query)
            if len(numbers) >= 2:
                v1, v2 = int(numbers[0]), int(numbers[1])
                res = v1 - v2
                if res > 0:
                    return f"💰 হিসাব সম্পন্ন: আপনার এখানে {res} টাকা লাভ বা অতিরিক্ত রয়েছে।"
                elif res < 0:
                    return f"📉 হিসাব সম্পন্ন: আপনার এখানে {abs(res)} টাকা ক্ষতি বা ঘাটতি হয়েছে।"
                else:
                    return "⚖️ হিসাব সম্পন্ন: আপনার লাভ বা ক্ষতি কিছুই হয়নি।"

        # গাণিতিক চিহ্নের মাধ্যমে জটিল অংক বা সমীকরণ সমাধান
        math_symbols = ['+', '-', '*', '/', '^', '(', ')', '=']
        if any(char in query for char in math_symbols) or query.isdigit():
            if '=' in query:
                # সমীকরণ সমাধান (যেমন: x+2=5)
                parts = query.split('=')
                equation = sympify(parts[0].strip() + "- (" + parts[1].strip() + ")")
                result = solve(equation)
                return f"🔢 সমীকরণের সমাধান: {result}"
            else:
                # সাধারণ বা জটিল ক্যালকুলেশন
                result = sympify(query)
                return f"🔢 গণিতের ফলাফল: {result}"
    except:
        return None
    return None

def get_wiki_info(query):
    """উইকিপিডিয়া থেকে তথ্য এবং বানান সংশোধন"""
    try:
        search_query = urllib.parse.quote(query)
        url = f"https://bn.wikipedia.org/w/api.php?action=opensearch&search={search_query}&limit=1&format=json"
        headers = {'User-Agent': 'XtremeAI/2.0'}
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if len(data) > 1 and data[1]:
                title = data[1][0]
                link = data[3][0]
                
                summary_url = f"https://bn.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title.replace(' ', '_'))}"
                req_s = urllib.request.Request(summary_url, headers=headers)
                with urllib.request.urlopen(req_s) as res_s:
                    info = json.loads(res_s.read().decode())
                    return {"text": f"🔍 আপনি কি বুঝিয়েছেন: {title}?\n📌 তথ্য: {info.get('extract')}", "url": link}
    except:
        return None
    return {"text": "❌ দুঃখিত, আমি আপনার প্রশ্নটি ঠিক বুঝতে পারিনি। আপনি আমার কাছে ঠিক কী জানতে চান? দয়া করে স্পষ্ট করে লিখুন।", "url": None}

def main():
    print("====================================")
    print("      🚀 XTREME AI PRO EDITION  ")
    print("      Status: Work In Progress...   ")
    print("====================================")
    print("বন্ধ করতে 'exit' লিখুন।\n")
    
    while True:
        user_input = input("👤 আপনি: ").strip()
        
        if user_input.lower() == 'exit':
            print("বিদায়! ভালো থাকবেন।")
            break
            
        # যদি ইনপুট খালি থাকে
        if not user_input:
            print("🤖 Xtreme AI: আপনি আমার কাছে কী জানতে চান বলুন? আপনি কি উইকিপিডিয়া প্রশ্ন করতে চান নাকি ম্যাথ সমাধান করতে চান?")
            continue
            
        # ১. সাধারণ চ্যাট (হাই/হ্যালো)
        if user_input.lower() in ["hi", "hello", "হাই", "হ্যালো"]:
            print("🤖 Xtreme AI: হ্যালো! আমি আপনার স্মার্ট অ্যাসিস্ট্যান্ট। আপনার গণিত বা সাধারণ জ্ঞানের প্রশ্নটি আমাকে করতে পারেন।")
            continue

        # ২. গণিত ও লজিক সমাধান
        math_res = solve_math_pro(user_input)
        if math_res:
            print(f"🤖 Xtreme AI: {math_res}")
            continue
            
        # ৩. উইকিপিডিয়া তথ্য
        print("⌛ তথ্য বিশ্লেষণ করা হচ্ছে...")
        result = get_wiki_info(user_input)
        if result:
            print(f"\n--- ফলাফল ---\n{result['text']}\n--------------")
            if result['url']:
                open_link = input("\n🔗 আপনি কি পুরো পেজটি ব্রাউজারে ওপেন করতে চান? (y/n): ").lower()
                if open_link == 'y':
                    webbrowser.open(result['url'])

if __name__ == "__main__":
    main()
