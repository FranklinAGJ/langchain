"""Interactive Bible-based motivational chatbot using LangChain + OpenAI"""
import os
import sys
import logging
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from langchain_openai import ChatOpenAI
from prompts import BIBLE_MOTIVATE_PROMPT
from utils import VerseManager, extract_keywords_from_input
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

class BibleChatBot:
    """Enhanced Bible chatbot with better UX and error handling."""
    
    def __init__(self):
        self.console = Console()
        self.verse_manager = VerseManager()
        self.llm: Optional[ChatOpenAI] = None
        self._setup_llm()
    
    def _setup_llm(self):
        """Initialize the LLM with error handling."""
        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            self.console.print(
                Panel(
                    "[red]Please set OPENAI_API_KEY in your environment or .env file.[/red]",
                    title="Configuration Error",
                    border_style="red"
                )
            )
            sys.exit(1)
        
        try:
            self.llm = ChatOpenAI(
                temperature=0.6,
                model="gpt-3.5-turbo",
                api_key=api_key
            )
            logger.info("LLM initialized successfully")
        except Exception as e:
            self.console.print(f"[red]Error initializing OpenAI: {e}[/red]")
            sys.exit(1)
    
    def _get_response(self, user_input: str) -> str:
        """Generate response with improved verse selection."""
        try:
            # Extract keywords for better verse matching
            keywords = extract_keywords_from_input(user_input)
            verse = self.verse_manager.pick_verse(keywords=keywords)
            
            # Use modern LangChain pattern
            chain = BIBLE_MOTIVATE_PROMPT | self.llm
            response = chain.invoke({
                'user_input': user_input,
                'verse_ref': verse['ref'],
                'verse_text': verse['text']
            })
            return response.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return ("I'm here with you in this moment. Sometimes we face challenges that feel overwhelming, "
                   "but remember: 'The LORD is my shepherd; I shall not want.' (Psalm 23:1) "
                   "Take a deep breath and know that you're not alone in this journey.")
    
    def _display_welcome(self):
        """Display welcome message with styling."""
        welcome_text = Text()
        welcome_text.append("Welcome to your Bible Companion\n", style="bold blue")
        welcome_text.append("You are not alone in your journey. Share what's on your heart,\n")
        welcome_text.append("and receive encouragement through God's word.\n\n")
        welcome_text.append("Commands: ", style="dim")
        welcome_text.append("'quit' or 'exit' to leave, 'help' for guidance", style="dim italic")
        
        self.console.print(Panel(welcome_text, border_style="blue", padding=(1, 2)))
    
    def _display_help(self):
        """Display help information."""
        help_text = Text()
        help_text.append("How to use this chatbot:\n\n", style="bold")
        help_text.append("• Share your feelings, struggles, or concerns\n")
        help_text.append("• Ask for encouragement or guidance\n")
        help_text.append("• Examples: 'I'm feeling anxious', 'I'm struggling with doubt', 'I need strength'\n\n")
        help_text.append("The bot will respond with empathy and a relevant Bible verse.\n")
        help_text.append("Type 'quit' or 'exit' when you're ready to leave.")
        
        self.console.print(Panel(help_text, title="Help", border_style="green"))
    
    def run(self):
        """Main chat loop with enhanced UX."""
        self._display_welcome()
        
        while True:
            try:
                user_input = Prompt.ask("\n[bold cyan]You[/bold cyan]").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ('quit', 'exit', 'q'):
                    self.console.print(
                        Panel(
                            "[green]Take care — God is with you always. Goodbye! 🙏[/green]",
                            border_style="green"
                        )
                    )
                    break
                
                if user_input.lower() in ('help', 'h', '?'):
                    self._display_help()
                    continue
                
                # Show thinking indicator
                with self.console.status("[dim]Reflecting on your words...[/dim]"):
                    response = self._get_response(user_input)
                
                # Display response in a styled panel
                self.console.print(
                    Panel(
                        response,
                        title="[bold blue]Encouragement[/bold blue]",
                        border_style="blue",
                        padding=(1, 2)
                    )
                )
                
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Goodbye! May God's peace be with you.[/yellow]")
                break
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                self.console.print("[red]I'm sorry, something went wrong. Please try again.[/red]")

def main():
    """Entry point for the Bible chatbot."""
    try:
        bot = BibleChatBot()
        bot.run()
    except Exception as e:
        console = Console()
        console.print(f"[red]Failed to start chatbot: {e}[/red]")
        sys.exit(1)

if __name__ == '__main__':
    main()
