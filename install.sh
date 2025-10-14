#!/bin/bash

FILE_PATH=$(find "$(pwd)" -name "__main__.py" | head -n 1)

if [ -z "$FILE_PATH" ]; then
    echo "__main__.py پیدا نشد!"
    exit 1
fi

DIR_PATH=$(dirname "$FILE_PATH")

ALIAS_CMD="alias tachi='python3 $DIR_PATH/__main__.py'"

grep -qxF "$ALIAS_CMD" ~/.zshrc || echo "$ALIAS_CMD" >> ~/.zshrc

source ~/.zshrc

echo "Alias 'tachi' has been added and is ready to use!"