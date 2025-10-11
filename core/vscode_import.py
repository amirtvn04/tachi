import os
import subprocess
from tachi.config.manager import config # type: ignore
from pathlib import Path
import json

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
