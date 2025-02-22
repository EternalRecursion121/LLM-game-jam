# Fantasy Text Adventure Game

An interactive choose-your-own-adventure game powered by Google's Gemini AI. The game features a persistent inventory system, dynamic storytelling, and an atmospheric interface.


## Setup

1. Clone the repository:
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

4. Create a `.env` file in the root directory with your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

To get a Gemini API key:
- Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
- Create or select a project
- Generate an API key
- Copy the key to your `.env` file

5. Run the application:
```bash
python rpg/main.py
```

6. Open your browser and navigate to:
```
http://localhost:5000
```

## Game Controls

- Read the story text and current situation
- Choose your actions by clicking one of the available options
- Monitor your inventory (health, gold, and items) as you progress
- The game maintains a history of your choices and adapts the story accordingly

## Technical Details

- Built with Flask web framework
- Uses Google's Gemini AI for dynamic storytelling
- Pydantic models for data validation
- Session-based state management
- Responsive design with custom CSS animations

## Requirements

See `requirements.txt` for a full list of dependencies. Key requirements:
- Python 3.7+
- Flask
- google-genai
- pydantic
- python-dotenv

## Development

To run in debug mode (recommended for development):
```bash
export FLASK_ENV=development  # On Windows use: set FLASK_ENV=development
python rpg/main.py
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

[MIT License](LICENSE)