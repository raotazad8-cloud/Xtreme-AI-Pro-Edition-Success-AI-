#!/bin/bash

echo "🚀 XTREAM AI PRO EDITION  ইন্সটল হচ্ছে..."

# পাইথন এবং প্রয়োজনীয় প্যাকেজ আপডেট
pkg update && pkg upgrade -y
pkg install python -y

# লাইব্রেরি ইনস্টল
pip install sympy

echo "✅ সবকিছু ঠিকঠাক ইনস্টল হয়েছে!"
echo "🤖 এআই চালু করতে লিখুন: python main.py"
