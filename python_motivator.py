"""A CLI app for programmers who need motivation — pairs technical empathy with Bible verses."""
import os
import sys
import click
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from langchain_openai import ChatOpenAI
from prompts import get_prompt_for_context
from utils import VerseManager, extract_keywords_from_input
from dotenv import load_dotenv

console = Console()

class ProgrammerMotivator:
    """Motivational support specifically designed for developers."""
    
    def __init__(self):
        self.verse_manager = VerseManager()
        self.llm: Optional[ChatOpenAI] = None
        self._setup_llm()
    
    def _setup_llm(self):
        """Initialize the LLM with error handling."""
        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            console.print("[red]Please set OPENAI_API_KEY in your environment or .env file.[/red]")
            sys.exit(1)
        
        try:
            self.llm = ChatOpenAI(
                temperature=0.5,
                model="gpt-3.5-turbo",
                api_key=api_key
            )
        except Exception as e:
            console.print(f"[red]Error initializing OpenAI: {e}[/red]")
            sys.exit(1)
    
    def get_motivation(self, issue: str, topic: Optional[str] = None) -> str:
        """Generate motivational response for programmer issues."""
        try:
            # Map common programmer issues to verse topics
            programmer_keywords = {
                'bug': ['patience', 'strength'],
                'stuck': ['help', 'strength'],
                'imposter': ['assurance', 'strength'],
                'overwhelmed': ['peace', 'rest'],
                'deadline': ['peace', 'strength'],
                'frustrated': ['patience', 'peace'],
                'tired': ['rest', 'strength'],
                'burnout': ['rest', 'peace'],
                'failure': ['hope', 'strength'],
                'rejected': ['assurance', 'hope'],
                'difficult': ['strength', 'help'],
                'complex': ['help', 'strength'],
            }
            
            # Extract keywords from the issue
            keywords = extract_keywords_from_input(issue)
            
            # Add programmer-specific keywords
            for word, tags in programmer_keywords.items():
                if word in issue.lower():
                    keywords.extend(tags)
            
            # Default to strength if no specific keywords found
            if not keywords:
                keywords = ['strength']
            
            verse = self.verse_manager.pick_verse(keywords=keywords)
            
            # Use modern LangChain pattern
            prompt = get_prompt_for_context("programmer")
            chain = prompt | self.llm
            response = chain.invoke({
                'user_input': issue,
                'verse_ref': verse['ref'],
                'verse_text': verse['text']
            })
            return response.content.strip()
            
        except Exception as e:
            console.print(f"[red]Error generating motivation: {e}[/red]")
            return ("Every developer faces challenges — it's part of the journey. 'Be strong and of a good courage; be not afraid, neither be thou dismayed: for the LORD thy God is with thee whithersoever thou goest.' (Joshua 1:9) Take a break, breathe, and remember that every expert was once a beginner.")

@click.command()
@click.option('--issue', '-i', help='Describe what\'s bothering you as a programmer')
@click.option('--interactive', '-I', is_flag=True, help='Run in interactive mode')
@click.option('--quick', '-q', is_flag=True, help='Get quick motivation for general coding struggles')
def main(issue: Optional[str], interactive: bool, quick: bool):
    """
    Python Developer Motivator — Biblical encouragement for coding challenges.
    
    Examples:
      python_motivator.py -i "stuck on a complex algorithm"
      python_motivator.py --quick
      python_motivator.py --interactive
    """
    motivator = ProgrammerMotivator()
    
    if quick:
        issue = "I'm feeling discouraged with my coding progress"
    elif interactive:
        console.print(Panel(
            Text("🚀 Developer Motivation Station 🚀\n\n", style="bold blue") +
            Text("Share your coding struggles and receive encouragement\n") +
            Text("tailored for developers, backed by biblical wisdom.\n\n") +
            Text("Type 'quit' to exit.", style="dim italic"),
            border_style="blue"
        ))
        
        while True:
            try:
                user_issue = console.input("\n[bold cyan]What's challenging you today?[/bold cyan] ").strip()
                
                if not user_issue:
                    continue
                
                if user_issue.lower() in ('quit', 'exit', 'q'):
                    console.print("[green]Keep coding with confidence! God is with you. 👨‍💻✨[/green]")
                    break
                
                with console.status("[dim]Crafting your encouragement...[/dim]"):
                    response = motivator.get_motivation(user_issue)
                
                console.print(Panel(
                    response,
                    title="[bold green]Developer Encouragement[/bold green]",
                    border_style="green",
                    padding=(1, 2)
                ))
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Happy coding! May your bugs be few and your commits be clean! 🐛➡️✨[/yellow]")
                break
        return
    
    if not issue:
        # Default interactive prompt
        console.print("[bold blue]Python Dev Motivator[/bold blue] — What's bothering you?")
        console.print("Examples: 'stuck on a bug', 'feeling imposter syndrome', 'overwhelmed by complexity'")
        issue = console.input("\n[cyan]Issue:[/cyan] ").strip()
        
        if not issue:
            issue = 'I feel stuck and discouraged with my coding.'
    
    # Generate and display motivation
    with console.status("[dim]Generating encouragement...[/dim]"):
        response = motivator.get_motivation(issue)
    
    console.print(Panel(
        response,
        title="[bold green]Developer Encouragement[/bold green]",
        border_style="green",
        padding=(1, 2)
    ))

if __name__ == '__main__':
    main()
