#!/bin/bash

# স্ক্রিন ক্লিয়ার করা
clear

# কালার কোড (আউটপুট সুন্দর করার জন্য)
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${CYAN}==========================================${NC}"
echo -e "${GREEN}    🚀 XTREME AI - AUTO INSTALLER PRO${NC}"
echo -e "${CYAN}==========================================${NC}"
echo -e "${YELLOW}শুরু হচ্ছে... অনুগ্রহ করে অপেক্ষা করুন।${NC}"

# ১. সিস্টেম আপডেট ও পাইথন চেক
echo -e "\n${CYAN}[১/৪] সিস্টেম আপডেট করা হচ্ছে...${NC}"
pkg update -y && pkg upgrade -y

echo -e "\n${CYAN}[২/৪] প্রয়োজনীয় প্যাকেজ ইনস্টল করা হচ্ছে...${NC}"
pkg install python git -y

# ২. পাইথন লাইব্রেরি ইনস্টল (Sympy & Googletrans)
echo -e "\n${CYAN}[৩/৪] পাইথন লাইব্রেরি সেটআপ করা হচ্ছে...${NC}"
echo -e "${YELLOW}Installing Sympy & Googletrans (4.0.0-rc1)...${NC}"
pip install --upgrade pip
pip install sympy googletrans==4.0.0-rc1

# ৩. ফাইল পারমিশন সেট করা
echo -e "\n${CYAN}[৪/৪] ফাইল পারমিশন কনফিগার করা হচ্ছে...${NC}"
chmod +x main.py
chmod +x update.sh

# ৪. সাকসেস মেসেজ
clear
echo -e "${GREEN}==========================================${NC}"
echo -e "${GREEN} ✅ ইন্সটলেশন সফলভাবে সম্পন্ন হয়েছে!${NC}"
echo -e "${GREEN}==========================================${NC}"
echo -e "${CYAN}ডেভেলপার: Raiyan Ibne Azad (Xtreme IT)${NC}"
echo -e "${YELLOW}------------------------------------------${NC}"
echo -e "${WHITE}এআই চালু করতে নিচের কমান্ডটি লিখুন:${NC}"
echo -e "${GREEN}python main.py${NC}"
echo -e "${YELLOW}------------------------------------------${NC}"
