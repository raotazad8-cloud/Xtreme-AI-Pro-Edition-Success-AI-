import urllib.request
import urllib.parse
import json
import re
import os
import threading
import time
import sys
import subprocess
import webbrowser 
from sympy import sympify, solve

# --- Project Configuration ---
VERSION = "3.6 Pro (Universal)"
DEVELOPER = "Raiyan Ibne Azad"

class XAI:
    def __init__(self):
        self.is_searching = False
        self.is_ai_online = True 
        self.history_file = "Chat_history.txt"

    def open_link(self, url):
        """System to open links on both Termux and PC"""
        try:
            # 1. Check if the environment is Termux
            if os.path.exists('/data/data/com.termux/files/usr/bin/termux-open-url'):
                subprocess.run(['termux-open-url', url])
            else:
                # 2. Open default browser for Windows/Linux/Mac
                webbrowser.open(url)
        except Exception as e:
            print(f"\n⚠️ Unable to open browser. Please copy the link:\n🔗 {url}")

    def save_history(self, user_input, ai_response):
        """Save chat and study notes"""
        with open(self.history_file, "a", encoding="utf-8") as f:
            t = time.strftime("%H:%M:%S")
            f.write(f"[{t}] User: {user_input}\nAI: {ai_response}\n{'-'*40}\n")

    def get_wiki(self, query):
        """Search Engine (For information retrieval)"""
        if not self.is_ai_online: return {"text": "⚠️ System is Offline.", "url": None}
        
        # Clean common phrases from the query
        clean = re.sub(r'\b(who is|what is|info|about|tell me)\b', '', query, flags=re.IGNORECASE).strip()
        
        try:
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(clean)}"
            req = urllib.request.Request(url, headers={'User-Agent': 'XAI-Universal-Bot'})
            with urllib.request.urlopen(req, timeout=7) as res:
                data = json.loads(res.read().decode())
                if data.get('type') == 'standard':
                    return {
                        "text": f"📚 Topic: {data['title']}\n📖 Info: {data['extract']}",
                        "url": data.get('content_urls', {}).get('desktop', {}).get('page')
                    }
                return {"text": "❌ No information found.", "url": None}
        except:
            return {"text": "⚠️ Network or Server error!", "url": None}

    def solve_math(self, query):
        """Math solving engine"""
        try:
            if '=' in query:
                parts = query.split('=')
                eq = sympify(parts[0].strip() + "-(" + parts[1].strip() + ")")
                return f"🔢 Algebra Solution: x = {solve(eq)}"
            if any(c in query for c in "+-*/^"):
                return f"🔢 Result: {sympify(query)}"
        except:
            return None

    def loader(self):
        """Processing animation"""
        chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        i = 0
        while self.is_searching:
            print(f"\r⚡ X-AI is searching {chars[i % len(chars)]}", end="", flush=True)
            i += 1
            time.sleep(0.1)
        print("\r", end="")

    def start(self):
        """Main Program Loop"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"\n{'═'*55}")
        print(f"      🎓 X AI {VERSION}")
        print(f"      Developer: {DEVELOPER}")
        print(f"{'═'*55}")
        print("Commands: 'cls', 'exit', 'turn off ai', 'turn on ai'")

        while True:
            cmd = input("\n👤 You: ").strip()
            if not cmd: continue
            if cmd.lower() in ['exit', 'quit', 'stop']: break
            if cmd.lower() == 'cls': os.system('clear' if os.name == 'posix' else 'cls'); continue
            
            if cmd.lower() == "turn off ai": self.is_ai_online = False; print("🛑 AI Disabled."); continue
            if cmd.lower() == "turn on ai": self.is_ai_online = True; print("🟢 AI Enabled."); continue

            if not self.is_ai_online:
                print("🤖 AI: [OFFLINE]"); continue

            math_res = self.solve_math(cmd)
            if math_res:
                print(f"🤖 AI: {math_res}")
                self.save_history(cmd, math_res)
                continue

            self.is_searching = True
            t = threading.Thread(target=self.loader)
            t.start()
            res = self.get_wiki(cmd)
            self.is_searching = False
            t.join()

            print(f"🤖 AI:\n{res['text']}")
            self.save_history(cmd, res['text'])

            # --- Universal Link System (y/n) ---
            if res.get('url'):
                print(f"\n🔗 Link: {res['url']}")
                choice = input("🌐 Open browser for more details? (y/n): ").lower().strip()
                if choice == 'y':
                    print("🚀 Opening browser...")
                    self.open_link(res['url'])
                else:
                    print("🆗 Noted.")

if __name__ == "__main__":
    XAI().start()
