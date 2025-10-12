import sys
from tachi.core.vscode_import import import_vscode_recent # type: ignore
from tachi.core.commands import ( # type: ignore
    add_project,
    remove_project,
    list_projects,
    open_project,
    search_projects,
    edit_project,
)
from tachi.config.manager import config # type: ignore
from tachi.core.utils import show_help # type: ignore

def main():
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1]
    name = sys.argv[2] if len(sys.argv) > 2 else None
    path = sys.argv[3] if len(sys.argv) > 3 else None
    rename = sys.argv[4] if len(sys.argv) > 4 else None

    if command == "add":
        return add_project(name, path)
    elif command == "remove":
        return remove_project(name)
    elif command == "list":
        return list_projects()
    elif command == "search":
        return search_projects(name)
    elif command == "edit":
        return edit_project(name, path, rename)
    elif command == "import":
        return import_vscode_recent()
    elif command == "help":
        return show_help()
    else:
        return open_project(command)
