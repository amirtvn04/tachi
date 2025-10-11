import subprocess

def run_command(cmd, cwd):
    print()
    if isinstance(cmd, list):
        subprocess.run(cmd, cwd=cwd, check=True)
    else:
        subprocess.run(cmd, cwd=cwd, check=True, shell=True, executable="/bin/zsh")
        
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