import urllib.request
import urllib.parse
import json
import webbrowser
import re
import os
import threading
import time
import sys
from sympy import sympify, solve

# --- Project Configuration ---
VERSION = "3.5"
DEVELOPER = "Raiyan Ibne Azad"
# সিক্রেট কি শুধু কোডের ভেতরেই থাকবে, লগইন লাগবে না
SECRET_KEY = "={admin@1_940388}=RaiyanIbneAzad2013#$_&-+()/*\"'':;!?~`|•√π÷×§∆£¢€¥^°{=}\%©®™✓]["

class XAI:
    def __init__(self):
        self.is_searching = False
        self.is_ai_online = True 
        self.history_file = "Chat_history.txt"

    def save_history(self, user_input, ai_response):
        """চ্যাট হিস্ট্রি অটোমেটিক সেভ করা"""
        with open(self.history_file, "a", encoding="utf-8") as f:
            f.write(f"User: {user_input}\nAI: {ai_response}\n{'-'*30}\n")

    def get_wiki(self, query):
        """উইকিপিডিয়া থেকে তথ্য এবং লিঙ্ক সংগ্রহ করা"""
        if not self.is_ai_online: return {"text": "⚠️ System Offline.", "url": None}
        
        clean = re.sub(r'\b(who is|what is|info|about|tell me)\b', '', query, flags=re.IGNORECASE).strip()
        
        try:
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(clean)}"
            req = urllib.request.Request(url, headers={'User-Agent': 'XAI-Bot'})
            with urllib.request.urlopen(req, timeout=5) as res:
                data = json.loads(res.read().decode())
                if data.get('type') == 'standard':
                    return {
                        "text": f"🔍 Topic: {data['title']}\n📌 Info: {data['extract']}",
                        "url": data.get('content_urls', {}).get('desktop', {}).get('page')
                    }
                return {"text": "❌ This is not found . ", "url": None}
        except:
            return {"text": "⚠️ Wrong !!!", "url": None}

    def solve_math(self, query):
        """গণিত সমাধান করার ইঞ্জিন"""
        try:
            if '=' in query:
                parts = query.split('=')
                eq = sympify(parts[0].strip() + "-(" + parts[1].strip() + ")")
                return f"🔢 Algebra: x = {solve(eq)}"
            if any(c in query for c in "+-*/^"):
                return f"🔢 Result: {sympify(query)}"
        except:
            return None

    def loader(self):
        """প্রসেসিং অ্যানিমেশন"""
        chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        i = 0
        while self.is_searching:
            print(f"\r⚡ X-AI Thinking {chars[i % len(chars)]}", end="", flush=True)
            i += 1
            time.sleep(0.1)
        print("\r", end="")

    def start(self):
        """প্রধান প্রোগ্রাম শুরু"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"\n{'═'*55}")
        print(f"      🚀 X AI VERSION {VERSION} (DIRECT ACCESS)")
        print(f"      Developer: {DEVELOPER}")
        print(f"{'═'*55}")
        print("Commands: 'cls', 'exit', 'turn off/on ai'")

        while True:
            cmd = input("\n👤 You: ").strip()
            if not cmd: continue
            if cmd.lower() in ['exit', 'quit']: break
            if cmd.lower() == 'cls': os.system('clear'); continue
            
            # সিস্টেম কন্ট্রোল
            if cmd.lower() == "turn off ai":
                self.is_ai_online = False
                print("🛑 AI System Disabled."); continue
            if cmd.lower() == "turn on ai":
                self.is_ai_online = True
                print("🟢 AI System Enabled."); continue

            if not self.is_ai_online:
                print("🤖 AI: [OFFLINE] System is turned off"); continue

            # গণিত চেক করা
            math_res = self.solve_math(cmd)
            if math_res:
                print(f"🤖 AI: {math_res}")
                self.save_history(cmd, math_res)
                continue

            # সার্চ ইঞ্জিন
            self.is_searching = True
            t = threading.Thread(target=self.loader)
            t.start()
            res = self.get_wiki(cmd)
            self.is_searching = False
            t.join()

            print(f"🤖 AI:\n{res['text']}")
            self.save_history(cmd, res['text'])

            if res.get('url'):
                print(f"\n🔗 Source: {res['url']}")
                if input("🌐 Open in browser? (y/n): ").lower() == 'y':
                    webbrowser.open(res['url'])

if __name__ == "__main__":
    XAI().start()
