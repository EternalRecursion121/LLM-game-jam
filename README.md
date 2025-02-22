# Fantasy Text Adventure Game Template

A customizable text adventure game template powered by Google's Gemini AI that provides a solid foundation for building AI-powered narrative games.

## Features

- Ready-to-use game engine
- AI-powered dynamic storytelling
- Persistent inventory and game state
- Atmospheric UI with animations
- Easy to customize and extend

## Project Structure

```
.
├── game/
│   ├── __init__.py
│   ├── models.py        # Data models
│   ├── game_logic.py    # Core game mechanics
│   ├── ai_interface.py  # AI interaction logic
│   ├── templates/       # HTML templates
│   │   └── game.html
│   └── static/         # CSS and JavaScript
│       └── style.css
├── main.py             # Application entry point
├── requirements.txt
└── README.md
```

## Setup

1. Clone the template:
```bash
git clone https://github.com/EternalRecursion121/LLM-game-jam.git
cd LLM-game-jam
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file:
```
GEMINI_API_KEY=your_api_key_here
```

To get a Gemini API key:
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key and paste it in your `.env` file

5. Run the game:
```bash
python main.py
```

## Customization Guide

### 1. Modify Game Content

Edit `game/game_logic.py` to customize:
- Starting conditions
- Game mechanics
- Victory/failure conditions

### 2. Adjust AI Behavior

Edit `game/ai_interface.py` to modify:
- Story generation prompts
- AI response parsing
- Choice generation

### 3. Change the Look and Feel

Edit `game/templates/game.html` and `game/static/style.css` to:
- Customize the UI
- Add new visual elements
- Modify animations

### 4. Extend Game Features

Some ideas to get you started:
- Add combat mechanics
- Implement a save/load system
- Create character classes
- Add multiplayer support
- Integrate different AI models

## Requirements

- Python 3.7+
- Flask
- google-genai
- pydantic
- python-dotenv

## Contributing

Feel free to:
- Fork and customize
- Submit bug fixes
- Suggest improvements
- Share your creations

## License

[MIT License](LICENSE) - Feel free to use this template for your projects!

## Acknowledgments

Built with:
- Google Gemini AI
- Flask
- Pydantic