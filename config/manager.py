import json
from pathlib import Path

CONFIG_FILE = Path(__file__).parent.parent / "tachi.json"

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
    return value