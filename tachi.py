#!/usr/bin/env python3

import sys
import subprocess
import json
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPT_DIR / "tachi.json"


def config(key, value=None):
    try:
        data = json.loads(CONFIG_FILE.read_text())
    except json.JSONDecodeError:
        data = {}

    if value is None:
        return data.get(key)

    data[key] = value
    CONFIG_FILE.write_text(json.dumps(data, indent=2))
    return value


def run_command(cmd, cwd):
    print()
    if isinstance(cmd, list):
        subprocess.run(cmd, cwd=cwd, check=True)
    else:
        subprocess.run(cmd, cwd=cwd, check=True, shell=True, executable="/bin/zsh")


def detect_auto_commands(path: Path):
    commands = []

    if (path / "docker-compose.override.yml").exists():
        commands += [
            "colima start",
            "docker-compose -f docker-compose.override.yml up -d",
        ]
    elif (path / "docker-compose.yml").exists():
        commands += [
            "colima start",
            "docker-compose up -d",
        ]

    return commands


def open_project(name):
    path_str = config(name)

    if not path_str:
        print(f"❌ Project '{name}' not found!")
        return

    path = Path(path_str)

    print(f"📂 Opening {name} in VS Code...")
    subprocess.run(
        ["/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code", path]
    )

    auto_commands = detect_auto_commands(path)

    for cmd in auto_commands:
        run_command(cmd, path)


def import_vscode_recent():
    vscode_db = os.path.expanduser(
        "~/Library/Application Support/Code/User/globalStorage/state.vscdb"
    )

    if not os.path.exists(vscode_db):
        print("❌ VSCode state file not found.")
        return

    try:
        result = subprocess.run(
            [
                "sqlite3",
                vscode_db,
                "SELECT value FROM ItemTable WHERE key='history.recentlyOpenedPathsList';",
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        entries = json.loads(result.stdout).get("entries", [])

        for entry in entries:
            if "folderUri" in entry:
                path = entry["folderUri"].replace("file://", "")
            elif "fileUri" in entry:
                path = entry["fileUri"].replace("file://", "")
            else:
                continue

            config(Path(path).name, path)

        print(f"✅ Imported {len(entries)} projects from VSCode")

    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print(f"❌ Error importing VSCode projects: {e}")


def main():
    if not CONFIG_FILE.exists():
        with CONFIG_FILE.open("w") as f:
            json.dump({}, f, indent=2)

    if len(sys.argv) < 2:
        print("Usage: tachi [project_name|add|add-vscode-data] [project_path]")
        return

    command = sys.argv[1]
    name = sys.argv[2] if len(sys.argv) > 2 else None
    path = sys.argv[3] if len(sys.argv) > 3 else None

    if command == "add":
        if not name:
            return import_vscode_recent()

        if not path:
            return

        return config(name, path)

    return open_project(command)


if __name__ == "__main__":
    main()
