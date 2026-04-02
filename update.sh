#!/bin/bash

# স্ক্রিন পরিষ্কার করা
clear

echo "=========================================="
echo "    🔄 XTREME AI AUTO-UPDATE SYSTEM"
echo "=========================================="

# ১. ইন্টারনেট চেক করা
echo "🌐 ইন্টারনেট কানেকশন চেক করা হচ্ছে..."
if ping -c 1 google.com &> /dev/null; then
    echo "✅ ইন্টারনেট আছে।"
else
    echo "❌ ইন্টারনেট নেই! আপডেট করতে ইন্টারনেট প্রয়োজন।"
    exit
fi

# ২. গিট থেকে লেটেস্ট কোড নামানো
echo "📥 গিটহাব থেকে নতুন ফাইল চেক করা হচ্ছে..."
git fetch --all
git reset --hard origin/main

# ৩. লাইব্রেরি আপডেট করা
echo "📦 লাইব্রেরি (Requirements) চেক করা হচ্ছে..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    pip install sympy
fi

# ৪. পারমিশন ঠিক করা
chmod +x main.py
chmod +x update.sh

echo ""
echo "=========================================="
echo "✅ আপডেট সম্পন্ন হয়েছে! ভার্সন: Upgraded Pro"
echo "🤖 এআই চালু করতে লিখুন: python main.py"
echo "=========================================="
