#!/bin/bash

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}🚀 Installing Tachi CLI...${NC}"

FILE_PATH=$(find "$(pwd)" -name "__main__.py" | head -n 1)

if [ -z "$FILE_PATH" ]; then
    echo -e "${RED}❌ __main__.py not found!${NC}"
    exit 1
fi

DIR_PATH=$(dirname "$FILE_PATH")
ALIAS_CMD="alias tachi='python3 $DIR_PATH/__main__.py'"

if [[ "$SHELL" == *"zsh"* ]]; then
    FILE=~/.zshrc
    SHELL_NAME="zsh"
    SOURCE_CMD="source ~/.zshrc"
elif [[ "$SHELL" == *"bash"* ]]; then
    if [ -f ~/.bash_profile ]; then
        FILE=~/.bash_profile
    elif [ -f ~/.bashrc ]; then
        FILE=~/.bashrc
    else
        FILE=~/.bash_profile
    fi
    SHELL_NAME="bash"
    SOURCE_CMD="source $FILE"
else
    FILE=~/.profile
    SHELL_NAME="default shell"
    SOURCE_CMD="source ~/.profile"
fi

echo -e "\n${YELLOW}📦 Installing required Python packages...${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 not found! Please install Python 3.${NC}"
    exit 1
fi

if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
else
    echo -e "${RED}❌ pip not found! Please install pip or pip3.${NC}"
    exit 1
fi

REQUIRED_PACKAGES=("rich" "prompt_toolkit" "inquirer")

for pkg in "${REQUIRED_PACKAGES[@]}"; do
    if python3 -m pip show "$pkg" &> /dev/null; then
        echo -e "${GREEN}✔ $pkg already installed.${NC}"
    else
        echo -e "${CYAN}➡ Installing $pkg using $PIP_CMD...${NC}"
        $PIP_CMD install "$pkg" --quiet
    fi
done

if grep -q "alias tachi=" "$FILE"; then
    CURRENT_ALIAS=$(grep "alias tachi=" "$FILE")
    if [ "$CURRENT_ALIAS" != "$ALIAS_CMD" ]; then
        sed -i.bak "s|$CURRENT_ALIAS|$ALIAS_CMD|" "$FILE"
        echo -e "${YELLOW}🔄 Updated existing alias in $FILE${NC}"
    else
        echo -e "${GREEN}✅ Alias 'tachi' already up to date in $FILE${NC}"
    fi
else
    echo "$ALIAS_CMD" >> "$FILE"
    echo -e "${GREEN}✅ Alias added to $FILE${NC}"
fi

if [ -f "${FILE}.bak" ]; then
    rm "${FILE}.bak"
fi

echo -e "\n${CYAN}🎯 Alias 'tachi' is ready to use in $SHELL_NAME!${NC}"
echo -e "${YELLOW}📝 Run '$SOURCE_CMD' or restart your terminal to apply changes.${NC}"
echo -e "${GREEN}✅ Installation complete.${NC}"
