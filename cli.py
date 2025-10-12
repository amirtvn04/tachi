import sys
from tachi.core.vscode_import import import_vscode_recent # type: ignore
from tachi.core.commands import ( # type: ignore
    add_project,
    remove_project,
    list_projects,
    open_projects,
    search_projects,
    edit_project,
)
from tachi.config.manager import config # type: ignore
from tachi.core.utils import show_help # type: ignore

def main():
    args = sys.argv[1:]
    
    if not args:
        show_help()
        return

    command = args[0]

    if command == "add" and len(args) >= 3:
        name, path = args[1], args[2]
        return add_project(name, path)
    
    elif command == "remove" and len(args) >= 2:
        return remove_project(args[1])
    
    elif command == "list":
        return list_projects()
    
    elif command == "search" and len(args) >= 2:
        return search_projects(args[1])
    
    elif command == "edit" and len(args) >= 4:
        name, path, new_name = args[1], args[2], args[3]
        return edit_project(name, path, new_name)
    
    elif command == "import":
        return import_vscode_recent()
    
    elif command == "help":
        return show_help()
    
    else:
        return open_projects(args)
