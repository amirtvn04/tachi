#!/usr/bin/env python3

import sys
import subprocess
import json
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPT_DIR / "tachi.json"


def config(key=None, value=None, delete=False):
    if not CONFIG_FILE.exists():
        CONFIG_FILE.write_text(json.dumps({}, indent=2))
    try:
        data = json.loads(CONFIG_FILE.read_text())
    except json.JSONDecodeError:
        data = {}

    if delete and key:
        if key in data:
            del data[key]
            CONFIG_FILE.write_text(json.dumps(data, indent=2))
            print(f"🗑️  Removed project '{key}' successfully.")
        else:
            print(f"❌ Project '{key}' not found.")
        return

    if key is None and value is None:
        return data

    if value is None:
        return data.get(key)

    data[key] = value
    CONFIG_FILE.write_text(json.dumps(data, indent=2))
    print(f"✅ Added project '{key}' -> '{value}'")
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
    path_str = config(key = name)

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

        count = 0
        for entry in entries:
            if "folderUri" in entry:
                path = entry["folderUri"].replace("file://", "")
            elif "fileUri" in entry:
                path = entry["fileUri"].replace("file://", "")
            else:
                continue

            if os.path.exists(path):
                config(key = Path(path).name, value = path)
                count += 1
                
        print(f"✅ Imported {count} projects from VSCode")
        return True

    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print(f"❌ Error importing VSCode projects: {e}")
        return False


def list_projects():
    data = config()
    if not data:
        print("📭 No projects registered yet.")
        return
    print("📁 Registered Projects:")
    for name, path in data.items():
        print(f"  - {name:15} → {path}")


def search_projects(keyword):
    data = config()
    results = {
        k: v
        for k, v in data.items()
        if keyword.lower() in k.lower() or keyword.lower() in v.lower()
    }
    if not results:
        print(f"🔍 No projects found matching '{keyword}'.")
        return
    print(f"🔍 Search results for '{keyword}':")
    for name, path in results.items():
        print(f"  - {name:15} → {path}")


def edit_project(name, new_path = None, new_name = None):
    current_path = config(key = name)
    if not current_path:
        print(f"❌ Project '{name}' not found!")
        return False
    
    data = config()
    
    if new_name and new_name != name:
        data[new_name] = current_path
        del data[name]
        print(f"✏️  Renamed project '{name}' to '{new_name}'")
        name = new_name
    
    if new_path:
        data[name] = new_path
        print(f"✏️  Updated path for project '{name}'")
    
    CONFIG_FILE.write_text(json.dumps(data, indent=2))
    return True


def show_help():
    print("""
Tachi - Project Manager 🗂️

Usage:
  tachi <project_name>                      Open project in VS Code
  tachi add <name> <path>                   Add new project
  tachi edit <name> [new_path] [new_name]   Edit project (optional new_name)
  tachi remove <name>                       Remove project
  tachi list                                List all projects
  tachi search <keyword>                    Search projects
  tachi import                              Import from VSCode recent
  tachi help                                Show this help

Examples:
  tachi add blog /Users/me/projects/blog
  tachi remove old-project
  tachi search api
  tachi my-react-app
""")


def main():
    if not CONFIG_FILE.exists():
        with CONFIG_FILE.open("w") as f:
            json.dump({}, f, indent=2)

    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1]
    name = sys.argv[2] if len(sys.argv) > 2 else None
    path = sys.argv[3] if len(sys.argv) > 3 else None
    rename = sys.argv[4] if len(sys.argv) > 4 else None

    if command == "add":
        if not name:
            return import_vscode_recent()

        if not path:
            return

        return config(key = name, value = path)

    elif command == "list":
        return list_projects()

    elif command == "remove":
        if not name:
            print("❌ Missing project name to remove.")
            return
        return config(key = name, delete = True)

    elif command == "search":
        if not name:
            print("❌ Missing search keyword.")
            return
        return search_projects(name)
    
    elif command == "edit":
        if not name:
            print("❌ Missing name.")
            return False
        return edit_project(name, path, rename)
    
    elif command == "help":
        return show_help()
    
    elif command == "import":
        return import_vscode_recent()
    
    else:
        return open_project(command)


if __name__ == "__main__":
    main()