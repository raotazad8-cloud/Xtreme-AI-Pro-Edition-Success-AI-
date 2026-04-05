import flet as ft
import urllib.request
import urllib.parse
import json
import re
import os
from datetime import datetime

# --- Constants & Config ---
AI_NAME = "Xtreme AI Pro"
SUB_NAME = "Success AI Pro Edition"
DB_FILE = "chat_history.json"
BRAND_IMG = "famous_photo.jpg"

class XtremeAI:
    def __init__(self):
        self.history = self.load_history()

    def load_history(self):
        if not os.path.exists(DB_FILE):
            with open(DB_FILE, "w", encoding="utf-8") as f:
                json.dump([], f)
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: return []

    def save_chat(self, q, a):
        chat_data = {"time": str(datetime.now()), "user": q, "ai": a}
        self.history.append(chat_data)
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=4)

    def get_ai_response(self, query):
        try:
            clean_q = re.sub(r'\b(who is|what is|info)\b', '', query, flags=re.IGNORECASE).strip()
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(clean_q)}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Xtreme-AI-Pro'})
            with urllib.request.urlopen(req, timeout=5) as res:
                data = json.loads(res.read().decode())
                return data.get('extract', "❌ No specific data found on the web.")
        except:
            return "⚠️ Connection Error! Please check your internet."

def main(page: ft.Page):
    ai = XtremeAI()
    page.title = AI_NAME
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#080b12" # Deep Blue-Black
    page.padding = 20

    chat_list = ft.Column(expand=True, scroll=ft.ScrollMode.ALWAYS, spacing=15)

    def send_click(e):
        if not user_input.value: return
        
        q = user_input.value
        user_input.value = ""
        
        # User Message
        chat_list.controls.append(ft.Text(f"👤 Master Raiyan: {q}", color="cyan", weight="bold"))
        page.update()

        # AI Response
        ans = ai.get_ai_response(q)
        ai.save_chat(q, ans)

        # Glass UI Bubble
        ai_bubble = ft.Container(
            content=ft.Text(f"🤖 AI: {ans}", color="white"),
            padding=20,
            border_radius=20,
            bgcolor=ft.colors.with_opacity(0.1, "white"),
            border=ft.border.all(1, ft.colors.with_opacity(0.2, "white")),
            blur=ft.Blur(15, 15),
        )
        chat_list.controls.append(ai_bubble)
        page.update()

    user_input = ft.TextField(
        hint_text="Ask Xtreme AI Pro...",
        expand=True,
        border_radius=30,
        bgcolor=ft.colors.with_opacity(0.05, "white"),
        on_submit=send_click
    )

    # Top Branding Row
    page.add(
        ft.Row([
            ft.Icon(ft.icons.BOLT, color="cyan", size=30),
            ft.Text(SUB_NAME, size=22, weight="bold", color="cyan")
        ]),
        ft.Divider(height=1, color="white24"),
        chat_list,
        ft.Row([user_input, ft.FloatingActionButton(icon=ft.icons.SEND, on_click=send_click, bgcolor="cyan", icon_color="black")])
    )

if __name__ == "__main__":
    ft.app(target=main)
