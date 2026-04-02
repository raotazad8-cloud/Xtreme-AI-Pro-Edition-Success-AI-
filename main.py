import urllib.request, urllib.parse, json, webbrowser, re, os, threading, time, sys
from sympy import sympify, solve

# --- Admin Configuration ---
VERSION = "3.5"
DEVELOPER = "Raiyan Ibne Azad"
ADMIN_USER = "Raiyan"
ADMIN_PASS = "Raiyan2013#"
SECRET_KEY = "={admin@1_940388}=RaiyanIbneAzad2013#$_&-+()/*\"'':;!?~`|•√π÷×§∆£¢€¥^°{=}\%©®™✓]["

class XAI:
    def __init__(self):
        self.is_searching = False
        self.is_ai_online = True 

    def login(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"\n{'═'*55}\n      🔐 {VERSION} ADMIN LOGIN SYSTEM\n{'═'*55}")
        user = input("👤 Username: ").strip()
        pwd = input("🔑 Password: ").strip()
        if user == ADMIN_USER and pwd == ADMIN_PASS:
            print("\n✅ Access Granted! Loading X-AI..."); time.sleep(1); return True
        else:
            print("\n❌ Access Denied! Invalid Credentials."); sys.exit()

    def get_wiki(self, query):
        if not self.is_ai_online: return {"text": "⚠️ System Offline.", "url": None}
        clean = re.sub(r'\b(who is|what is|info|about|tell me)\b', '', query, flags=re.IGNORECASE).strip()
        try:
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(clean)}"
            req = urllib.request.Request(url, headers={'User-Agent': 'XAI-Admin'})
            with urllib.request.urlopen(req, timeout=5) as res:
                data = json.loads(res.read().decode())
                if data.get('type') == 'standard':
                    return {
                        "text": f"🔍 Topic: {data['title']}\n📌 Info: {data['extract']}",
                        "url": data.get('content_urls', {}).get('desktop', {}).get('page')
                    }
                return {"text": "❌ Not found.", "url": None}
        except: return {"text": "⚠️ Network error.", "url": None}

    def solve_math(self, query):
        try:
            if '=' in query:
                parts = query.split('=')
                eq = sympify(parts[0].strip() + "-(" + parts[1].strip() + ")")
                return f"🔢 Algebra: x = {solve(eq)}"
            if any(c in query for c in "+-*/^"):
                return f"🔢 Result: {sympify(query)}"
        except: return None

    def loader(self):
        chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        i = 0
        while self.is_searching:
            print(f"\r⚡ Processing {chars[i % len(chars)]}", end="", flush=True)
            i += 1; time.sleep(0.1)
        print("\r", end="")

    def start(self):
        if not self.login(): return
        os.system('clear')
        print(f"\n{'═'*55}\n      🚀 X AI VERSION {VERSION} (ADMIN MODE)\n{'═'*55}")
        
        while True:
            cmd = input("\n👤 You: ").strip()
            if not cmd: continue
            if cmd.lower() in ['exit', 'quit']: break
            if cmd.lower() == 'cls': os.system('clear'); continue
            if cmd.lower() == "turn off ai": self.is_ai_online = False; print("🛑 AI OFF"); continue
            if cmd.lower() == "turn on ai": self.is_ai_online = True; print("🟢 AI ON"); continue

            if not self.is_ai_online:
                print("🤖 AI: [OFFLINE] System is disabled."); continue

            math_res = self.solve_math(cmd)
            if math_res: print(f"🤖 AI: {math_res}"); continue

            self.is_searching = True
            t = threading.Thread(target=self.loader); t.start()
            res = self.get_wiki(cmd)
            self.is_searching = False; t.join()

            print(f"🤖 AI:\n{res['text']}")
            if res.get('url'):
                print(f"🔗 Source: {res['url']}")
                if input("🌐 Open link in browser? (y/n): ").lower() == 'y':
                    webbrowser.open(res['url'])

if __name__ == "__main__":
    XAI().start()
