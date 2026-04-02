#!/bin/bash
clear
echo "🛠️ X-AI System Updating..."
git reset --hard
git pull origin main
chmod +x *
echo "✅ All files upgraded! Run 'python main.py' to start."
