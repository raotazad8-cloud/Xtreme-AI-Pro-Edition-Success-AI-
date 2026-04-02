import urllib.request
import urllib.parse
import json
import webbrowser
import re
import os
from datetime import datetime
from sympy import sympify, solve

# --- Advanced Features ---

def save_to_history(user_input, ai_response):
    """Saves conversations to a local log file"""
    with open("chat_history.txt", "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}]\nUser: {user_input}\nAI: {ai_response}\n{'-'*30}\n")

def unit_converter(query):
    """Handles basic unit conversions"""
    try:
        # Temperature Conversion logic
        if "to f" in query.lower():
            num = re.findall(r"[-+]?\d*\.\d+|\d+", query)[0]
            res = (float(num) * 9/5) + 32
            return f"🌡️ {num}°C is equal to {res}°F"
        elif "to c" in query.lower():
            num = re.findall(r"[-+]?\d*\.\d+|\d+", query)[0]
            res = (float(num) - 32) * 5/9
            return f"🌡️ {num}°F is equal to {round(res, 2)}°C"
    except:
        return None
    return None

def get_wiki_info(query):
    """Enhanced Wikipedia Search with better keyword extraction"""
    try:
        # Intelligent keyword cleaning
        clean_query = re.sub(r'\b(who is|what is|about|tell me|info|search for|hey|please)\b', '', query, flags=re.IGNORECASE).strip()
        if not clean_query: return {"text": "❌ Please provide a topic to search.", "url": None}
        
        encoded_query = urllib.parse.quote(clean_query)
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded_query}"
        headers = {'User-Agent': 'XtremeAI/Pro_Upgrade (Education)'}
        
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode())
            if data.get('type') == 'standard':
                title = data.get('title')
                extract = data.get('extract')
                link = data.get('content_urls', {}).get('desktop', {}).get('page')
                return {"text": f"🔍 Topic: {title}\n📌 Info: {extract}", "url": link}
            else:
                return {"text": "❌ Sorry, I couldn't find a direct match. Try being more specific.", "url": None}
    except Exception:
        return {"text": "⚠️ Search failed. Please check your internet connection.", "url": None}

def solve_math(query):
    """Handles math, algebra, and business logic"""
    try:
        # Business Logic
        if any(word in query.lower() for word in ["profit", "loss", "income", "expense", "balance"]):
            numbers = re.findall(r'\d+', query)
            if len(numbers) >= 2:
                v1, v2 = int(numbers[0]), int(numbers[1])
                res = v1 - v2
                status = "Profit" if res > 0 else "Loss/Deficit"
                return f"💰 Status: {status} of {abs(res)}"

        # General Math & Algebra
        math_symbols = ['+', '-', '*', '/', '^', '(', ')', '=']
        if any(char in query for char in math_symbols) or query.isdigit():
            if '=' in query:
                parts = query.split('=')
                eq = sympify(parts[0].strip() + "-(" + parts[1].strip() + ")")
                return f"🔢 Algebra Solution: {solve(eq)}"
            return f"🔢 Result: {sympify(query)}"
    except: return None

# --- Main Engine ---

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    print("\n" + "═"*50)
    print("      🚀 XTREME AI - ULTIMATE PRO EDITION")
    print("      Features: Math | Wiki | Conversion | Logs")
    print("═"*50)
    print("Commands: 'history' to view logs, 'exit' to quit.")
    
    while True:
        user_input = input("\n👤 You: ").strip()
        
        if not user_input: continue
        if user_input.lower() in ['exit', 'quit']:
            print("🤖 Xtreme AI: Shutting down. Goodbye!")
            break
            
        if user_input.lower() == 'history':
            if os.path.exists("chat_history.txt"):
                print("\n📜 --- Recent Chat Logs ---")
                with open("chat_history.txt", "r") as f:
                    print(f.read())
            else:
                print("🤖 Xtreme AI: No history found yet.")
            continue

        # 1. Unit Conversion Check
        conv_res = unit_converter(user_input)
        if conv_res:
            print(f"🤖 Xtreme AI: {conv_res}")
            save_to_history(user_input, conv_res)
            continue

        # 2. Math Solving Check
        math_res = solve_math(user_input)
        if math_res:
            print(f"🤖 Xtreme AI: {math_res}")
            save_to_history(user_input, math_res)
            continue
            
        # 3. Wikipedia Search
        print("⌛ Analyzing request...")
        result = get_wiki_info(user_input)
        print(f"\n🤖 Xtreme AI:\n{result['text']}")
        save_to_history(user_input, result['text'])
        
        if result.get('url'):
            choice = input("\n🔗 Open full source in browser? (y/n): ").lower()
            if choice == 'y':
                webbrowser.open(result['url'])

if __name__ == "__main__":
    main()
