#!/usr/bin/env python3
"""
Setup script for Bible Motivator
Handles installation and configuration
"""
import os
import sys
import subprocess
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

console = Console()

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3.8, 0):
        console.print("[red]Error: Python 3.8 or higher is required.[/red]")
        console.print(f"[yellow]Current version: {sys.version}[/yellow]")
        return False
    return True

def install_dependencies():
    """Install required dependencies."""
    console.print("[blue]Installing dependencies...[/blue]")
    
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True, capture_output=True)
        console.print("[green]✅ Dependencies installed successfully![/green]")
        return True
    except subprocess.CalledProcessError as e:
        console.print(f"[red]❌ Failed to install dependencies: {e}[/red]")
        return False

def setup_api_key():
    """Setup OpenAI API key."""
    env_file = Path(".env")
    
    if env_file.exists():
        with open(env_file, 'r') as f:
            content = f.read()
            if "OPENAI_API_KEY" in content and "test_key_for_now" not in content:
                console.print("[green]✅ API key already configured![/green]")
                return True
    
    console.print(Panel(
        "OpenAI API Key Setup\n\n"
        "To use the AI-powered features, you need an OpenAI API key.\n"
        "You can get one from: https://platform.openai.com/api-keys\n\n"
        "Note: You can skip this and use offline mode instead.",
        title="API Key Setup",
        border_style="blue"
    ))
    
    if not Confirm.ask("Do you want to configure your OpenAI API key now?"):
        console.print("[yellow]Skipping API key setup. You can use offline mode or configure it later.[/yellow]")
        return True
    
    api_key = Prompt.ask("Enter your OpenAI API key", password=True).strip()
    
    if not api_key:
        console.print("[yellow]No API key provided. You can configure it later.[/yellow]")
        return True
    
    try:
        with open(".env", "w") as f:
            f.write(f"OPENAI_API_KEY={api_key}\n")
        console.print("[green]✅ API key saved successfully![/green]")
        return True
    except Exception as e:
        console.print(f"[red]❌ Failed to save API key: {e}[/red]")
        return False

def run_tests():
    """Run the test suite."""
    console.print("[blue]Running tests...[/blue]")
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", "-v"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            console.print("[green]✅ All tests passed![/green]")
            return True
        else:
            console.print("[red]❌ Some tests failed![/red]")
            console.print(result.stdout)
            console.print(result.stderr)
            return False
    except FileNotFoundError:
        console.print("[yellow]⚠️  pytest not found, but that's okay for basic usage.[/yellow]")
        return True

def create_desktop_shortcut():
    """Create desktop shortcut (optional)."""
    if not Confirm.ask("Create desktop shortcut for easy access?"):
        return
    
    try:
        current_dir = Path.cwd()
        
        if sys.platform == "darwin":  # macOS
            shortcut_content = f'''#!/bin/bash
cd "{current_dir}"
python launcher.py
'''
            shortcut_path = Path.home() / "Desktop" / "Bible Motivator.command"
            with open(shortcut_path, "w") as f:
                f.write(shortcut_content)
            os.chmod(shortcut_path, 0o755)
            
        elif sys.platform == "win32":  # Windows
            import winshell
            from win32com.client import Dispatch
            
            shortcut_path = Path.home() / "Desktop" / "Bible Motivator.lnk"
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(str(shortcut_path))
            shortcut.Targetpath = sys.executable
            shortcut.Arguments = f'"{current_dir / "launcher.py"}"'
            shortcut.WorkingDirectory = str(current_dir)
            shortcut.save()
            
        else:  # Linux
            shortcut_content = f'''[Desktop Entry]
Version=1.0
Type=Application
Name=Bible Motivator
Comment=Spiritual encouragement and support
Exec=python "{current_dir / "launcher.py"}"
Path={current_dir}
Terminal=true
Categories=Utility;
'''
            shortcut_path = Path.home() / "Desktop" / "bible-motivator.desktop"
            with open(shortcut_path, "w") as f:
                f.write(shortcut_content)
            os.chmod(shortcut_path, 0o755)
        
        console.print(f"[green]✅ Desktop shortcut created: {shortcut_path}[/green]")
        
    except Exception as e:
        console.print(f"[yellow]⚠️  Could not create desktop shortcut: {e}[/yellow]")

def main():
    """Main setup function."""
    console.print(Panel(
        "🙏 Bible Motivator Setup\n\n"
        "Welcome! This script will help you set up the Bible Motivator application.\n"
        "This includes installing dependencies, configuring API keys, and running tests.",
        title="Setup",
        border_style="blue"
    ))
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Setup API key
    setup_api_key()
    
    # Run tests
    run_tests()
    
    # Create desktop shortcut
    create_desktop_shortcut()
    
    # Final message
    console.print(Panel(
        "[green]🎉 Setup completed successfully![/green]\n\n"
        "You can now run the application using:\n"
        "• [cyan]python launcher.py[/cyan] - Choose between different modes\n"
        "• [cyan]python bible_gui.py[/cyan] - GUI application\n"
        "• [cyan]python bible_chat.py[/cyan] - CLI chatbot\n"
        "• [cyan]python offline_mode.py[/cyan] - Works without internet\n\n"
        "Enjoy your spiritual journey! 🙏",
        title="Setup Complete",
        border_style="green"
    ))
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Setup cancelled by user.[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]Setup failed: {e}[/red]")
        sys.exit(1)