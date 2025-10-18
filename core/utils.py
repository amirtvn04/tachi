import subprocess
from rich.console import Console

console = Console()

def run_command(cmd, cwd):
    print()
    if isinstance(cmd, list):
        subprocess.run(cmd, cwd=cwd, check=True)
    else:
        subprocess.run(cmd, cwd=cwd, check=True, shell=True, executable="/bin/zsh")
        
def show_help():
    console.print("""
✨ [bold cyan]Tachi - Smart Project Launcher & Manager[/bold cyan] 🗂️
───────────────────────────────────────────────
Tachi is a simple Command-Line Interface (CLI) tool for managing projects.
It allows you to add projects, list them, and manage configuration settings.
The project is designed in a modular way for easy maintenance and scalability.

[bold]Usage:[/bold]
  tachi (command) (options)

[bold]Commands:[/bold]
  📂  [cyan]tachi <project_name>[/cyan]              
        → Instantly open a project by name
  ➕  [cyan]tachi add <name> <path>[/cyan]           
        → Register a new project with its directory path
  📝  [cyan]tachi edit <name> [new_path] [new_name][/cyan]  
        → Edit project name or path
  ❌  [cyan]tachi remove <name>[/cyan]               
        → Remove a registered project
  📜  [cyan]tachi list[/cyan]                       
        → View all saved projects (scrollable view)
  🔍  [cyan]tachi search <keyword>[/cyan]           
        → Search projects interactively with fuzzy matching
  ⚙️  [cyan]tachi import[/cyan]                     
        → Import projects automatically from VSCode recent list
  🧠  [cyan]tachi manage[/cyan]                     
        → Open full interactive manager (select, edit, remove)  
  💡  [cyan]tachi help[/cyan]                       
        → Show this help menu

[bold]Examples:[/bold]
  tachi add blog /Users/me/projects/blog
  tachi remove old-project
  tachi search dashboard
  tachi open my-react-app
  tachi manage
""")
