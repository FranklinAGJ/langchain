"""
Modern GUI Bible Motivator using CustomTkinter
Beautiful, user-friendly interface for spiritual encouragement
"""
import os
import sys
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext
from typing import Optional
import customtkinter as ctk
from langchain_openai import ChatOpenAI
from prompts import BIBLE_MOTIVATE_PROMPT, get_prompt_for_context
from utils import VerseManager, extract_keywords_from_input
from dotenv import load_dotenv

# Configure CustomTkinter
ctk.set_appearance_mode("dark")  # "dark" or "light"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

class BibleMotivatorGUI:
    """Modern GUI for Bible-based motivation and encouragement."""
    
    def __init__(self):
        self.root = ctk.CTk()
        self.verse_manager = VerseManager()
        self.llm: Optional[ChatOpenAI] = None
        self.current_mode = "general"  # "general" or "programmer"
        
        self.setup_window()
        self.setup_llm()
        self.create_widgets()
        
    def setup_window(self):
        """Configure the main window."""
        self.root.title("Bible Motivator - Spiritual Encouragement")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (900 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"900x700+{x}+{y}")
        
    def setup_llm(self):
        """Initialize the LLM with error handling."""
        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key or api_key == "test_key_for_now":
            self.show_api_key_dialog()
            return
            
        try:
            self.llm = ChatOpenAI(
                temperature=0.6,
                model="gpt-3.5-turbo",
                api_key=api_key
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize OpenAI: {str(e)}")
            
    def show_api_key_dialog(self):
        """Show dialog to enter API key."""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("OpenAI API Key Required")
        dialog.geometry("500x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (300 // 2)
        dialog.geometry(f"500x300+{x}+{y}")
        
        # Content
        ctk.CTkLabel(
            dialog, 
            text="OpenAI API Key Required",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)
        
        ctk.CTkLabel(
            dialog,
            text="Please enter your OpenAI API key to use this application.\nYou can get one from: https://platform.openai.com/api-keys",
            font=ctk.CTkFont(size=12),
            wraplength=400
        ).pack(pady=10)
        
        self.api_key_entry = ctk.CTkEntry(
            dialog,
            placeholder_text="sk-...",
            width=400,
            show="*"
        )
        self.api_key_entry.pack(pady=20)
        
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(pady=20)
        
        ctk.CTkButton(
            button_frame,
            text="Save & Continue",
            command=lambda: self.save_api_key(dialog),
            width=120
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_frame,
            text="Exit",
            command=self.root.quit,
            width=120,
            fg_color="gray"
        ).pack(side="left", padx=10)
        
    def save_api_key(self, dialog):
        """Save the API key and initialize LLM."""
        api_key = self.api_key_entry.get().strip()
        if not api_key:
            messagebox.showerror("Error", "Please enter a valid API key")
            return
            
        # Save to .env file
        try:
            with open('.env', 'w') as f:
                f.write(f"OPENAI_API_KEY={api_key}\n")
            
            # Initialize LLM
            self.llm = ChatOpenAI(
                temperature=0.6,
                model="gpt-3.5-turbo",
                api_key=api_key
            )
            
            dialog.destroy()
            messagebox.showinfo("Success", "API key saved successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save API key: {str(e)}")
            
    def create_widgets(self):
        """Create and arrange all GUI widgets."""
        # Main container
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="🙏 Bible Motivator",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=15)
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Find encouragement and strength through God's word",
            font=ctk.CTkFont(size=14)
        )
        subtitle_label.pack(pady=(0, 15))
        
        # Mode selection
        mode_frame = ctk.CTkFrame(main_frame)
        mode_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            mode_frame,
            text="Choose your context:",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 5))
        
        mode_button_frame = ctk.CTkFrame(mode_frame, fg_color="transparent")
        mode_button_frame.pack(pady=(5, 15))
        
        self.general_button = ctk.CTkButton(
            mode_button_frame,
            text="General Support",
            command=lambda: self.set_mode("general"),
            width=150
        )
        self.general_button.pack(side="left", padx=10)
        
        self.programmer_button = ctk.CTkButton(
            mode_button_frame,
            text="Developer Support",
            command=lambda: self.set_mode("programmer"),
            width=150,
            fg_color="gray"
        )
        self.programmer_button.pack(side="left", padx=10)
        
        # Chat area
        chat_frame = ctk.CTkFrame(main_frame)
        chat_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Chat history
        self.chat_display = ctk.CTkTextbox(
            chat_frame,
            height=300,
            font=ctk.CTkFont(size=12),
            wrap="word"
        )
        self.chat_display.pack(fill="both", expand=True, padx=15, pady=(15, 10))
        
        # Input area
        input_frame = ctk.CTkFrame(chat_frame, fg_color="transparent")
        input_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.input_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Share what's on your heart...",
            font=ctk.CTkFont(size=12),
            height=40
        )
        self.input_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.input_entry.bind("<Return>", self.send_message)
        
        self.send_button = ctk.CTkButton(
            input_frame,
            text="Send",
            command=self.send_message,
            width=80,
            height=40
        )
        self.send_button.pack(side="right")
        
        # Status bar
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="Ready to provide encouragement",
            font=ctk.CTkFont(size=10)
        )
        self.status_label.pack(pady=(0, 10))
        
        # Add welcome message
        self.add_welcome_message()
        
    def set_mode(self, mode):
        """Set the application mode (general or programmer)."""
        self.current_mode = mode
        
        if mode == "general":
            self.general_button.configure(fg_color=["#3B8ED0", "#1F6AA5"])
            self.programmer_button.configure(fg_color="gray")
            self.input_entry.configure(placeholder_text="Share what's on your heart...")
        else:
            self.programmer_button.configure(fg_color=["#3B8ED0", "#1F6AA5"])
            self.general_button.configure(fg_color="gray")
            self.input_entry.configure(placeholder_text="Describe your coding challenge...")
            
    def add_welcome_message(self):
        """Add welcome message to chat."""
        welcome_text = """Welcome to Bible Motivator! 🙏

I'm here to provide encouragement and support through God's word. Whether you're facing general life challenges or specific programming difficulties, share what's on your heart and receive personalized encouragement with relevant Bible verses.

Choose your context above and start sharing your thoughts.

Commands:
• Type 'clear' to clear the chat
• Type 'verse' to get a random encouraging verse
• Type 'help' for more guidance

You are not alone in your journey. ✨
"""
        self.chat_display.insert("end", welcome_text)
        self.chat_display.insert("end", "\n" + "="*50 + "\n\n")
        
    def send_message(self, event=None):
        """Send user message and get response."""
        message = self.input_entry.get().strip()
        if not message:
            return
            
        # Clear input
        self.input_entry.delete(0, "end")
        
        # Handle special commands
        if message.lower() == 'clear':
            self.chat_display.delete("1.0", "end")
            self.add_welcome_message()
            return
        elif message.lower() == 'verse':
            self.show_random_verse()
            return
        elif message.lower() == 'help':
            self.show_help()
            return
            
        # Add user message to chat
        self.chat_display.insert("end", f"You: {message}\n\n")
        self.chat_display.see("end")
        
        # Check if LLM is available
        if not self.llm:
            self.chat_display.insert("end", "Bot: Please configure your OpenAI API key first.\n\n")
            self.chat_display.see("end")
            return
            
        # Show thinking status
        self.status_label.configure(text="Reflecting on your words...")
        self.send_button.configure(state="disabled", text="...")
        
        # Get response in background thread
        threading.Thread(target=self.get_response_async, args=(message,), daemon=True).start()
        
    def get_response_async(self, message):
        """Get AI response in background thread."""
        try:
            # Extract keywords for better verse matching
            keywords = extract_keywords_from_input(message)
            verse = self.verse_manager.pick_verse(keywords=keywords)
            
            # Get appropriate prompt
            if self.current_mode == "programmer":
                prompt = get_prompt_for_context("programmer")
            else:
                prompt = BIBLE_MOTIVATE_PROMPT
                
            # Generate response
            chain = prompt | self.llm
            response = chain.invoke({
                'user_input': message,
                'verse_ref': verse['ref'],
                'verse_text': verse['text']
            })
            
            # Update UI in main thread
            self.root.after(0, self.display_response, response.content.strip())
            
        except Exception as e:
            fallback_response = self.get_fallback_response(message)
            self.root.after(0, self.display_response, fallback_response)
            
    def display_response(self, response):
        """Display the AI response in the chat."""
        self.chat_display.insert("end", f"Bot: {response}\n\n")
        self.chat_display.insert("end", "-" * 30 + "\n\n")
        self.chat_display.see("end")
        
        # Reset UI
        self.status_label.configure(text="Ready to provide encouragement")
        self.send_button.configure(state="normal", text="Send")
        
    def get_fallback_response(self, message):
        """Get fallback response when AI is unavailable."""
        keywords = extract_keywords_from_input(message)
        verse = self.verse_manager.pick_verse(keywords=keywords)
        
        return (f"I hear you, and I want you to know that you're not alone. "
                f"Here's an encouraging verse for you:\n\n"
                f'"{verse["text"]}" - {verse["ref"]}\n\n'
                f"Take heart and remember that God is with you in every challenge.")
                
    def show_random_verse(self):
        """Show a random encouraging verse."""
        verse = self.verse_manager.pick_verse()
        verse_text = f'Random Verse:\n\n"{verse["text"]}" - {verse["ref"]}\n\n'
        self.chat_display.insert("end", verse_text)
        self.chat_display.insert("end", "-" * 30 + "\n\n")
        self.chat_display.see("end")
        
    def show_help(self):
        """Show help information."""
        help_text = """Help & Commands:

• General Mode: Share your feelings, struggles, or concerns
• Developer Mode: Describe coding challenges, bugs, or technical frustrations
• 'clear' - Clear the chat history
• 'verse' - Get a random encouraging Bible verse
• 'help' - Show this help message

Examples:
- "I'm feeling anxious about tomorrow"
- "I'm stuck on a complex algorithm"
- "I feel overwhelmed with work"
- "My code isn't working and I'm frustrated"

The bot will respond with empathy and relevant Bible verses to encourage you.

"""
        self.chat_display.insert("end", help_text)
        self.chat_display.insert("end", "-" * 30 + "\n\n")
        self.chat_display.see("end")
        
    def run(self):
        """Start the GUI application."""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.root.quit()

def main():
    """Entry point for the GUI application."""
    try:
        app = BibleMotivatorGUI()
        app.run()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start application: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()