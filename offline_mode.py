"""
Offline Bible Motivator - Works without OpenAI API
Provides encouragement using pre-written responses and Bible verses
"""
import random
from typing import Dict, List
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from utils import VerseManager, extract_keywords_from_input

console = Console()

class OfflineBibleMotivator:
    """Offline version that provides encouragement without AI."""
    
    def __init__(self):
        self.verse_manager = VerseManager()
        self.response_templates = self._load_response_templates()
        
    def _load_response_templates(self) -> Dict[str, List[str]]:
        """Load pre-written response templates for different situations."""
        return {
            'general': [
                "I hear the weight in your words, and I want you to know that you're not alone. {verse_text} ({verse_ref}). Take comfort in knowing that God sees your struggle and is with you every step of the way.",
                
                "Your feelings are valid, and it's okay to feel overwhelmed sometimes. Remember: {verse_text} ({verse_ref}). Take a deep breath and trust that this difficult moment will pass.",
                
                "I can sense you're going through a challenging time. Here's a reminder of God's love for you: {verse_text} ({verse_ref}). You are stronger than you know, and you're never walking alone.",
                
                "Thank you for sharing what's on your heart. In times like these, I find comfort in these words: {verse_text} ({verse_ref}). May this verse bring you peace and strength today.",
                
                "Life can feel overwhelming, but remember that you're held by a love that never fails. {verse_text} ({verse_ref}). Take one moment at a time, and trust in God's faithfulness."
            ],
            
            'programmer': [
                "Every developer faces moments like this - it's part of the journey of growth. {verse_text} ({verse_ref}). Take a step back, breathe, and remember that even the most complex problems have solutions.",
                
                "Coding challenges can be frustrating, but they're also opportunities to grow stronger. {verse_text} ({verse_ref}). Sometimes the best debugging happens when we step away and return with fresh eyes.",
                
                "I understand the frustration of hitting technical walls. Remember: {verse_text} ({verse_ref}). Every expert was once a beginner, and every problem you solve makes you more capable.",
                
                "Programming can feel isolating when you're stuck, but you're part of a community that understands. {verse_text} ({verse_ref}). Don't hesitate to ask for help - collaboration often leads to breakthroughs.",
                
                "Technical challenges test our patience and perseverance. Here's encouragement: {verse_text} ({verse_ref}). Take a break, clear your mind, and approach the problem with renewed focus."
            ],
            
            'anxiety': [
                "Anxiety can feel overwhelming, but you don't have to face it alone. {verse_text} ({verse_ref}). Try taking slow, deep breaths and focusing on what you can control right now.",
                
                "I understand how anxiety can make everything feel uncertain. Remember: {verse_text} ({verse_ref}). Ground yourself in the present moment and trust that you have the strength to get through this.",
                
                "Anxious thoughts can spiral quickly, but you have the power to interrupt them. {verse_text} ({verse_ref}). Consider talking to someone you trust or practicing mindfulness to find peace."
            ],
            
            'strength': [
                "You're asking for strength, which shows incredible courage. {verse_text} ({verse_ref}). Strength isn't about never falling - it's about getting back up each time.",
                
                "Sometimes we need to be reminded of the strength we already possess. {verse_text} ({verse_ref}). You've overcome challenges before, and you have what it takes to overcome this one too.",
                
                "Seeking strength is a sign of wisdom, not weakness. {verse_text} ({verse_ref}). Draw from the well of God's endless strength, and know that you're capable of more than you realize."
            ]
        }
    
    def get_response(self, user_input: str, mode: str = "general") -> str:
        """Generate an encouraging response based on user input."""
        # Extract keywords to determine the best response category
        keywords = extract_keywords_from_input(user_input)
        
        # Determine response category
        category = "general"
        if mode == "programmer":
            category = "programmer"
        elif any(word in keywords for word in ['anxiety', 'anxious', 'worried']):
            category = "anxiety"
        elif any(word in keywords for word in ['strength', 'weak', 'tired']):
            category = "strength"
        
        # Get appropriate verse
        verse = self.verse_manager.pick_verse(keywords=keywords)
        
        # Select response template
        templates = self.response_templates.get(category, self.response_templates['general'])
        template = random.choice(templates)
        
        # Format response
        response = template.format(
            verse_text=verse['text'],
            verse_ref=verse['ref']
        )
        
        return response
    
    def run_interactive(self):
        """Run interactive offline mode."""
        self._display_welcome()
        
        while True:
            try:
                user_input = Prompt.ask("\n[bold cyan]You[/bold cyan]").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ('quit', 'exit', 'q'):
                    console.print(
                        Panel(
                            "[green]Take care — God is with you always. Goodbye! 🙏[/green]",
                            border_style="green"
                        )
                    )
                    break
                
                if user_input.lower() in ('help', 'h', '?'):
                    self._display_help()
                    continue
                
                if user_input.lower() == 'verse':
                    self._show_random_verse()
                    continue
                
                # Determine mode based on input
                mode = "programmer" if any(word in user_input.lower() for word in 
                                        ['code', 'bug', 'programming', 'developer', 'coding']) else "general"
                
                # Generate response
                response = self.get_response(user_input, mode)
                
                # Display response
                console.print(
                    Panel(
                        response,
                        title="[bold blue]Encouragement[/bold blue]",
                        border_style="blue",
                        padding=(1, 2)
                    )
                )
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Goodbye! May God's peace be with you.[/yellow]")
                break
            except Exception as e:
                console.print(f"[red]An error occurred: {e}[/red]")
    
    def _display_welcome(self):
        """Display welcome message."""
        welcome_text = Text()
        welcome_text.append("Welcome to Bible Motivator (Offline Mode)\n", style="bold blue")
        welcome_text.append("You are not alone in your journey. Share what's on your heart,\n")
        welcome_text.append("and receive encouragement through God's word.\n\n")
        welcome_text.append("This offline mode works without an internet connection!\n\n")
        welcome_text.append("Commands: ", style="dim")
        welcome_text.append("'quit' to exit, 'help' for guidance, 'verse' for random verse", style="dim italic")
        
        console.print(Panel(welcome_text, border_style="blue", padding=(1, 2)))
    
    def _display_help(self):
        """Display help information."""
        help_text = Text()
        help_text.append("How to use offline mode:\n\n", style="bold")
        help_text.append("• Share your feelings, struggles, or concerns\n")
        help_text.append("• Mention coding/programming for developer-focused responses\n")
        help_text.append("• Examples: 'I'm feeling anxious', 'stuck on a bug', 'need strength'\n\n")
        help_text.append("Commands:\n")
        help_text.append("• 'verse' - Get a random Bible verse\n")
        help_text.append("• 'help' - Show this help\n")
        help_text.append("• 'quit' - Exit the application\n\n")
        help_text.append("Note: This mode provides pre-written responses and doesn't require internet.")
        
        console.print(Panel(help_text, title="Help", border_style="green"))
    
    def _show_random_verse(self):
        """Show a random encouraging verse."""
        verse = self.verse_manager.pick_verse()
        verse_text = f'"{verse["text"]}" - {verse["ref"]}'
        
        console.print(
            Panel(
                verse_text,
                title="[bold green]Encouraging Verse[/bold green]",
                border_style="green",
                padding=(1, 2)
            )
        )

def main():
    """Entry point for offline mode."""
    try:
        motivator = OfflineBibleMotivator()
        motivator.run_interactive()
    except Exception as e:
        console.print(f"[red]Failed to start offline mode: {e}[/red]")

if __name__ == '__main__':
    main()