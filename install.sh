#!/bin/bash
clear

# UI Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}==========================================${NC}"
echo -e "${GREEN}    🚀 XTREME AI - ENGLISH INSTALLER${NC}"
echo -e "${CYAN}==========================================${NC}"

echo "Updating system..."
pkg update -y && pkg upgrade -y
pkg install python git -y

echo -e "\n${GREEN}📦 Installing Sympy (Math Library)...${NC}"
pip install sympy

# Fixing permissions
chmod +x main.py
chmod +x update.sh

echo -e "\n${GREEN}✅ Installation Successful!${NC}"
echo -e "To start the AI, type: ${CYAN}python main.py${NC}"
