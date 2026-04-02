#!/bin/bash
clear
echo "🚀 Installing X AI 3.0 Pro Requirements..."
apt update && apt upgrade -y
pkg install python git -y
pip install -r requirements.txt
chmod +x main.py update.sh install.sh
echo "✅ Installation Success! Run 'python main.py' to login."
