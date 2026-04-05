import flet as ft
import urllib.request
import urllib.parse
import json
import re
import os
from datetime import datetime

# --- Configuration ---
AI_NAME = "Xtreme AI Pro"
SUB_NAME = "Success AI Pro Edition"
DB_FILE = "customer_chats.json"

class XtremeAI:
    def __init__(self):
        self.load_history()

    def load_history(self):
        if not os.path.exists(DB_FILE):
            with open(DB_FILE, "w", encoding="utf-8") as f:
                json.dump([], f)
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: return []

    def save_chat(self, q, a):
        history = self.load_history()
        history.append({"time": str(datetime.now()), "user": q, "ai": a})
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4)

    def get_response(self, query):
        try:
            # Cleaning the search query
            clean = re.sub(r'\b(who|what|info|about)\b', '', query, flags=re.IGNORECASE).strip()
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(clean)}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Xtreme-AI-Customer'})
            with urllib.request.urlopen(req, timeout=7) as res:
                data = json.loads(res.read().decode())
                return data.get('extract', "❌ I couldn't find a direct answer. Please try different keywords.")
        except:
            return "⚠️ Connection error. Please check your internet and try again."

def main(page: ft.Page):
    ai = XtremeAI()
    page.title = AI_NAME
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#080b12" # Futuristic Dark Blue
    page.padding = 20

    chat_display = ft.Column(expand=True, scroll=ft.ScrollMode.ALWAYS, spacing=15)

    def send_msg(e):
        user_q = user_input.value.strip()
        if not user_q: return

        # User Question
        chat_display.controls.append(
            ft.Row([
                ft.Icon(ft.icons.PERSON, color="cyan", size=20),
                ft.Text(f"You: {user_q}", color="cyan", weight="bold")
            ])
        )
        user_input.value = ""
        page.update()

        # AI Loading & Response
        ans = ai.get_response(user_q)
        ai.save_chat(user_q, ans)

        # Glass Effect AI Bubble
        ai_bubble = ft.Container(
            content=ft.Text(f"🤖 {AI_NAME}: {ans}", color="white"),
            padding=15,
            border_radius=15,
            bgcolor=ft.colors.with_opacity(0.1, "white"),
            border=ft.border.all(1, ft.colors.with_opacity(0.2, "white")),
            blur=ft.Blur(10, 10),
        )
        chat_display.controls.append(ai_bubble)
        page.update()

    user_input = ft.TextField(
        hint_text="Type your question here...",
        expand=True,
        border_radius=30,
        bgcolor=ft.colors.with_opacity(0.05, "white"),
        on_submit=send_msg
    )

    # UI Header
    page.add(
        ft.Row([
            ft.Icon(ft.icons.AUTO_AWESOME, color="cyan"),
            ft.Text(SUB_NAME, size=20, weight="bold", color="cyan")
        ]),
        ft.Divider(height=1, color="white24"),
        chat_display,
        ft.Row([
            user_input, 
            ft.FloatingActionButton(icon=ft.icons.SEND, on_click=send_msg, bgcolor="cyan", icon_color="black")
        ])
    )

if __name__ == "__main__":
    ft.app(target=main)
