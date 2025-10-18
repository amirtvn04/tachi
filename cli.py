import sys
from core.vscode_import import import_vscode_recent 
from core.interactive import (
    manage_projects, list_projects,
    search_projects_rich,
    remove_or_edit_project,
)
from core.commands import ( 
    add_project,
    open_projects,
)
from core.utils import show_help 

def main():
    args = sys.argv[1:]
    
    if not args:
        manage_projects()
        return

    command = args[0]

    if command == "add" and len(args) >= 3:
        name, path = args[1], args[2]
        return add_project(name, path)
    
    elif command == "list":
        return list_projects()
    
    elif command == "search" and len(args) >= 1:
        search_projects_rich()
    
    elif command == "edit" and len(args) >= 1:
        remove_or_edit_project()
    
    elif command == "import":
        return import_vscode_recent()
    
    elif command == "manage":
        return manage_projects()
    
    elif command == "help":
        return show_help()
    
    else:
        return open_projects(args)
