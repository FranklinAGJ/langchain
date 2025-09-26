# Bible Motivator — AI-Powered Spiritual Encouragement 🙏

A thoughtfully designed Python application that combines **LangChain + OpenAI** with biblical wisdom to provide personalized encouragement and support. Features two specialized interfaces: a general Bible chatbot for emotional support and a developer-focused motivator for coding challenges.

## ✨ Features

### Core Functionality
- **Smart Verse Selection**: Advanced keyword matching to find the most relevant Bible verses
- **Contextual Responses**: Tailored prompts for general support vs. programmer-specific challenges  
- **Rich UI Experience**: Beautiful console interface with colors, panels, and status indicators
- **Error Handling**: Robust error handling with graceful fallbacks
- **Extensible Design**: Easy to add more verses, customize prompts, or swap AI providers

### Two Specialized Apps
1. **`bible_chat.py`** - Interactive chatbot for general emotional and spiritual support
2. **`python_motivator.py`** - CLI tool specifically designed for programmers facing coding challenges

### Enhanced Verse Database
- 25+ carefully selected Bible verses (KJV, public domain)
- Intelligent tagging system for better matching
- Support for topic-based and keyword-based selection

## 🚀 Quick Start

### Automated Setup (Recommended)
```bash
# Clone and navigate to the project
git clone <your-repo-url>
cd bible-motivator

# Run the setup script
python setup.py
```

The setup script will:
- Install all dependencies
- Help configure your OpenAI API key
- Run tests to verify everything works
- Optionally create a desktop shortcut

### Manual Installation
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure API key (optional - you can use offline mode)
cp .env.example .env
# Edit .env and add your API key: OPENAI_API_KEY=sk-your-key-here
```

## 💬 Usage

### Easy Launcher (Recommended)
```bash
python launcher.py
```
Choose from:
1. **GUI Application** - Modern graphical interface
2. **Bible Chat CLI** - Interactive terminal chatbot  
3. **Developer Motivator CLI** - Programmer-focused support
4. **Offline Mode** - Works without internet/API key
5. **Run Tests** - Verify everything works

### Individual Applications

#### Modern GUI Application
```bash
python bible_gui.py
```
Features:
- Beautiful modern interface with dark/light themes
- Real-time chat with AI responses
- Mode switching (General/Developer support)
- Built-in help and random verse features
- API key configuration dialog

#### Interactive Bible Chat (CLI)
```bash
python bible_chat.py
```
Features:
- Rich terminal interface with colors and panels
- Continuous conversation mode
- Smart verse selection based on your input
- Help commands and guidance

#### Developer Motivator (CLI)
```bash
# Interactive mode
python python_motivator.py --interactive

# Quick one-off motivation
python python_motivator.py -i "stuck on a complex algorithm"

# Quick general encouragement
python python_motivator.py --quick
```

#### Offline Mode (No Internet Required)
```bash
python offline_mode.py
```
Features:
- Works completely offline
- Pre-written encouraging responses
- Smart verse matching
- No API key required

## 🛠️ Development

### Project Structure
```
bible-motivator/
├── bible_chat.py          # Main chatbot application
├── python_motivator.py    # Developer-focused CLI tool
├── prompts.py            # LangChain prompt templates
├── utils.py              # Verse management and utilities
├── config.py             # Configuration management
├── bible_verses.json     # Verse database
├── tests/                # Test suite
│   ├── test_utils.py
│   └── test_prompts.py
├── requirements.txt      # Dependencies
└── README.md
```

### Running Tests
```bash
# Run all tests
python run_tests.py

# Or use pytest directly
python -m pytest

# Run specific test file
python -m pytest tests/test_utils.py -v
```

### Configuration Options
Create a `.env` file to customize behavior:
```bash
OPENAI_API_KEY=your-key-here
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_TEMPERATURE=0.6
RESPONSE_MAX_WORDS=200
USE_RICH_UI=true
LOG_LEVEL=INFO
```

## 🔧 Customization

### Adding New Verses
Edit `bible_verses.json`:
```json
{
  "ref": "Your Reference",
  "text": "Your verse text here",
  "tags": ["relevant", "keywords", "for", "matching"]
}
```

### Customizing Prompts
Modify templates in `prompts.py`:
- `BIBLE_MOTIVATE_PROMPT` - General encouragement
- `PROGRAMMER_MOTIVATE_PROMPT` - Developer-specific support

### Extending Functionality
The `VerseManager` class in `utils.py` provides:
- `pick_verse(topic=None, keywords=None)` - Smart verse selection
- `get_verses_by_tag(tag)` - Filter by specific tags
- `search_verses(query)` - Text-based search

## 🧪 Technical Details

### Dependencies
- **LangChain**: AI framework for prompt management
- **OpenAI**: GPT-3.5-turbo for response generation
- **Rich**: Beautiful terminal UI components
- **Click**: Command-line interface framework
- **pytest**: Testing framework

### AI Model Usage
- Model: GPT-3.5-turbo (configurable)
- Temperature: 0.6 for balanced creativity/consistency
- Max tokens: 300 for concise responses
- Fallback responses for API failures

## 📝 Examples

### General Support
```
You: I'm feeling overwhelmed with everything going on
Bot: I can hear the weight you're carrying right now, and it's completely understandable to feel overwhelmed when life feels like too much...
```

### Developer Support  
```
Issue: stuck on a complex algorithm
Response: Every developer hits walls with complex problems — it's actually a sign you're tackling meaningful challenges...
```

## ⚠️ Important Notes

- **API Costs**: Uses OpenAI API (small cost per interaction)
- **Content Review**: AI-generated responses should be reviewed for sensitive contexts
- **Bible Translation**: Uses KJV (public domain)
- **Privacy**: No conversation data is stored or transmitted beyond OpenAI API calls

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

This project is open source. Bible verses are from the King James Version (public domain). Please review AI-generated content for appropriateness in your specific context.

---

*"Cast all your anxiety on him because he cares for you." - 1 Peter 5:7*
