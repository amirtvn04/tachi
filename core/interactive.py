from InquirerPy import inquirer
from rich.console import Console
from rich.table import Table
from config.manager import (config, CONFIG_FILE)
from core.commands import open_projects
from core.vscode_import import import_vscode_recent
from core.utils import show_help
import json

console = Console()

def save_config(data):
    CONFIG_FILE.write_text(json.dumps(data, indent=2))

def list_projects():
    data = config()
    if not data:
        console.print("[yellow]📭 No projects found.[/yellow]")
        return

    table = Table(title="📦 Registered Projects", show_lines=True)
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Path", style="magenta")

    for name, path in data.items():
        table.add_row(f"📁 {name}", path)

    console.print(table)


def select_projects_inquirer():
    data = config()
    if not data:
        console.print("[yellow]📭 No projects found.[/yellow]")
        return []

    try:
        choices = [
            {"name": f"📁 {name} → {path}", "value": name}
            for name, path in data.items()
        ]

        selected = inquirer.checkbox(
            message="📂 Select projects to open:",
            choices=choices,
            instruction="(Use ↑/↓ to move, Space to select, Enter to confirm)",
        ).execute()

        if selected:
            console.print(f"[green]✅ Opening:[/green] {', '.join(selected)}")
            open_projects(selected)
        else:
            console.print("[yellow]No project selected.[/yellow]")

    except KeyboardInterrupt:
        console.print("\n[yellow]↩️ Returning to previous menu...[/yellow]")
        return

def remove_or_edit_project():
    data = config()
    if not data:
        console.print("[yellow]📭 No projects found.[/yellow]")
        return

    try:
        choices = [{"name": f"📁 {name} → {path}", "value": name} for name, path in data.items()]
        name = inquirer.select(
            message="🛠 Select a project to edit/remove:",
            choices=choices,
            default=None,
        ).execute()

        action = inquirer.select(
            message=f"⚙️ What do you want to do with '{name}'?",
            choices=["✏️ Edit project", "🗑 Delete project", "❌ Cancel"],
        ).execute()

        if action == "🗑 Delete project":
            confirm = inquirer.confirm(message=f"Are you sure you want to delete '{name}'?", default=False).execute()
            if confirm:
                del data[name]
                save_config(data)
                console.print(f"[red]🗑 Deleted project:[/red] {name}")
            else:
                console.print("[yellow]Cancelled.[/yellow]")

        elif action == "✏️ Edit project":
            new_name = inquirer.text(message=f"New name (press Enter to keep '{name}'):", default=name).execute()
            new_path = inquirer.text(message=f"New path (press Enter to keep current path):", default=data[name]).execute()

            if new_name != name:
                data[new_name] = data.pop(name)
            data[new_name] = new_path
            save_config(data)
            console.print(f"[green]✅ Updated project:[/green] {new_name}")

        else:
            console.print("[yellow]Cancelled.[/yellow]")
            
    except KeyboardInterrupt:
        console.print("\n[yellow]↩️ Returning to previous menu...[/yellow]")
        return

def search_projects_rich():
    data = config()
    if not data:
        console.print("[yellow]📭 No projects found.[/yellow]")
        return
    try:
        project = inquirer.fuzzy(
            message="🔎 Search for a project:",
            choices=[f"{name} → {path}" for name, path in data.items()],
            instruction="Type to search and press Enter to select",
        ).execute()

        if project:
            selected_name = project.split(" → ")[0]
            open_projects([selected_name])
        
    except KeyboardInterrupt:
        console.print("\n[yellow]↩️ Returning to previous menu...[/yellow]")
        return

def manage_projects():
    try:
        while True:
            action = inquirer.select(
                message="🚀 What do you want to do?",
                choices=[
                    "📜 List projects",
                    "📂 Open projects",
                    "🔍 Search projects",
                    "🛠  Edit or remove project",
                    "📭 Import projects",
                    "🚨 Help",
                ],
                instruction="(Use ↑/↓ to navigate, Enter to select, Ctrl+C to exit)",
            ).execute()

            if action == "📜 List projects":
                list_projects()
                
            elif action == "📂 Open projects":
                select_projects_inquirer()
                
            elif action == "🛠  Edit or remove project":
                remove_or_edit_project()
                
            elif action == "📭 Import projects":
                import_vscode_recent()
                
            elif action == "🔍 Search projects":
                search_projects_rich()
                
            else:
                show_help()
                break
            
    except KeyboardInterrupt:
        console.print("\n[red]❌ Program interrupted. Exiting...[/red]")
        raise SystemExit(0)
