import subprocess
import json
from pathlib import Path
from tachi.config.manager import (config, CONFIG_FILE) # type: ignore
from tachi.core.utils import run_command # type: ignore

def add_project(name, path):
    if not name or not path:
        print("Usage: tachi add <name> <path>")
        return
    config(name, str(Path(path).resolve()))
    print(f"✅ Added project '{name}' at '{path}'")

def remove_project(name):
    if not name:
        print("Usage: tachi remove <name>")
        return
    config(name, delete=True)

def list_projects():
    data = config()
    if not data:
        print("📭 No projects registered yet.")
        return
    print("📭 Registered Projects:")
    for name, path in data.items():
        print(f"📁 {name} → {path}")

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