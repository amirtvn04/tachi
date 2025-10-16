#!/bin/bash

FILE_PATH=$(find "$(pwd)" -name "__main__.py" | head -n 1)

if [ -z "$FILE_PATH" ]; then
    echo "❌ __main__.py not found!"
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

if grep -q "alias tachi=" "$FILE"; then
    CURRENT_ALIAS=$(grep "alias tachi=" "$FILE")
    if [ "$CURRENT_ALIAS" != "$ALIAS_CMD" ]; then
        sed -i.bak "s|$CURRENT_ALIAS|$ALIAS_CMD|" "$FILE"
        echo "🔄 Updated existing alias in $FILE"
    else
        echo "✅ Alias 'tachi' already up to date in $FILE"
    fi
else
    echo "$ALIAS_CMD" >> "$FILE"
    echo "✅ Alias added to $FILE"
fi

if [ -f "${FILE}.bak" ]; then
    rm "${FILE}.bak"
fi

echo "🎯 Alias 'tachi' is ready to use in $SHELL_NAME!"
echo "📝 Run '$SOURCE_CMD' or restart your terminal to apply changes."
