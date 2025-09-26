#!/usr/bin/env python3
"""
Bible Motivator Launcher
Choose between CLI and GUI versions
"""
import sys
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def show_menu():
    """Display the main menu."""
    title = Text()
    title.append("🙏 Bible Motivator Launcher", style="bold blue")
    
    menu_text = Text()
    menu_text.append("Choose your preferred interface:\n\n", style="bold")
    menu_text.append("1. ", style="cyan")
    menu_text.append("GUI Application", style="bold")
    menu_text.append(" - Modern graphical interface\n")
    menu_text.append("2. ", style="cyan") 
    menu_text.append("Bible Chat CLI", style="bold")
    menu_text.append(" - Interactive terminal chatbot\n")
    menu_text.append("3. ", style="cyan")
    menu_text.append("Developer Motivator CLI", style="bold")
    menu_text.append(" - Quick programmer support\n")
    menu_text.append("4. ", style="cyan")
    menu_text.append("Offline Mode", style="bold")
    menu_text.append(" - Works without internet/API key\n")
    menu_text.append("5. ", style="cyan")
    menu_text.append("Run Tests", style="bold")
    menu_text.append(" - Test the application\n")
    menu_text.append("6. ", style="cyan")
    menu_text.append("Exit", style="bold")
    menu_text.append("\n")
    
    console.print(Panel(title, border_style="blue"))
    console.print(Panel(menu_text, title="Options", border_style="green"))

def main():
    """Main launcher function."""
    while True:
        console.clear()
        show_menu()
        
        try:
            choice = console.input("\n[bold cyan]Enter your choice (1-6):[/bold cyan] ").strip()
            
            if choice == "1":
                console.print("[green]Starting GUI application...[/green]")
                subprocess.run([sys.executable, "bible_gui.py"])
                
            elif choice == "2":
                console.print("[green]Starting Bible Chat CLI...[/green]")
                subprocess.run([sys.executable, "bible_chat.py"])
                
            elif choice == "3":
                console.print("[green]Starting Developer Motivator...[/green]")
                subprocess.run([sys.executable, "python_motivator.py", "--interactive"])
                
            elif choice == "4":
                console.print("[green]Starting Offline Mode...[/green]")
                subprocess.run([sys.executable, "offline_mode.py"])
                
            elif choice == "5":
                console.print("[green]Running tests...[/green]")
                subprocess.run([sys.executable, "run_tests.py"])
                console.input("\n[dim]Press Enter to continue...[/dim]")
                
            elif choice == "6":
                console.print("[yellow]Goodbye! May God's peace be with you.[/yellow]")
                break
                
            else:
                console.print("[red]Invalid choice. Please enter 1-6.[/red]")
                console.input("\n[dim]Press Enter to continue...[/dim]")
                
        except KeyboardInterrupt:
            console.print("\n[yellow]Goodbye! May God's peace be with you.[/yellow]")
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            console.input("\n[dim]Press Enter to continue...[/dim]")

if __name__ == "__main__":
    main()