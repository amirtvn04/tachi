import subprocess
from pathlib import Path
from config.manager import config
from rich.console import Console
from core.utils import run_command

console = Console()

def add_project(name, path):
    if not name or not path:
        print("Usage: tachi add <name> <path>")
        return
    config(name, str(Path(path).resolve()))
    print(f"✅ Added project '{name}' at '{path}'")

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

def open_projects(names):
    for name in names:
        open_project(name)

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
        
