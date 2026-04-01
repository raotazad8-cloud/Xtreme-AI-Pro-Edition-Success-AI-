import urllib.request
import urllib.parse
import json
import webbrowser
import re
from sympy import sympify, solve

def get_wiki_info(query):
    """Fetches real-time info from English Wikipedia"""
    try:
        # Filter out common stop words to improve search accuracy
        clean_query = re.sub(r'\b(who is|what is|about|tell me|info|search for)\b', '', query, flags=re.IGNORECASE).strip()
        encoded_query = urllib.parse.quote(clean_query)
        
        # Wikipedia Summary API (English)
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded_query}"
        headers = {'User-Agent': 'XtremeAI/8.0 (Education Project)'}
        
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode())
            if data.get('type') == 'standard':
                title = data.get('title')
                extract = data.get('extract')
                link = data.get('content_urls', {}).get('desktop', {}).get('page')
                return {"text": f"🔍 Topic: {title}\n📌 Info: {extract}", "url": link}
            else:
                return {"text": "❌ Sorry, I couldn't find any information on this topic.", "url": None}
    except:
        return {"text": "⚠️ Information not found or Network error.", "url": None}

def solve_math(query):
    """Solves advanced math equations using Sympy"""
    try:
        # Profit and Loss logic for business calculations
        if any(word in query.lower() for word in ["profit", "loss", "income", "expense"]):
            numbers = re.findall(r'\d+', query)
            if len(numbers) >= 2:
                v1, v2 = int(numbers[0]), int(numbers[1])
                res = v1 - v2
                status = "Profit" if res > 0 else "Loss"
                return f"💰 Calculation: You have a {status} of {abs(res)}."

        # Equation Solving Logic
        math_symbols = ['+', '-', '*', '/', '^', '(', ')', '=']
        if any(char in query for char in math_symbols) or query.isdigit():
            if '=' in query:
                parts = query.split('=')
                eq = sympify(parts[0].strip() + "-(" + parts[1].strip() + ")")
                return f"🔢 Equation Result: {solve(eq)}"
            return f"🔢 Math Result: {sympify(query)}"
    except:
        return None

def main():
    print("\n" + "="*45)
    print("      🚀 XTREME AI (ENGLISH PRO EDITION)")
    print("      Status: Online | Mode: High Stability")
    print("      Developer: Raiyan Ibne Azad")
    print("="*45)
    print("Type 'exit' to close the program.")
    
    while True:
        user_input = input("\n👤 You: ").strip()
        if user_input.lower() in ['exit', 'quit', 'stop']:
            print("🤖 Xtreme AI: Goodbye! Have a great day.")
            break
        if not user_input: continue

        # 1. Math Solving
        math_res = solve_math(user_input)
        if math_res:
            print(f"🤖 Xtreme AI: {math_res}")
            continue
            
        # 2. Wikipedia Search
        print("⌛ Searching Wikipedia...")
        result = get_wiki_info(user_input)
        print(f"\n🤖 Xtreme AI:\n{result['text']}")
        
        if result.get('url'):
            opt = input("\n🔗 Read more on Browser? (y/n): ").lower()
            if opt == 'y': webbrowser.open(result['url'])

if __name__ == "__main__":
    main()
