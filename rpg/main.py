from flask import Flask, jsonify, request, render_template_string, session
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from typing import List, Optional
from google import genai 
from dataclasses import dataclass

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev')  # Add a secret key for sessions

# Pydantic models
class Inventory(BaseModel):
    items: List[str]
    health: int
    gold: int

class GameState(BaseModel):
    current_location: str
    description: str
    choices: List[str]
    inventory: Inventory
    game_over: bool

# HTML template
GAME_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Whispers of the Forest</title>
    <link href="https://fonts.googleapis.com/css2?family=IM+Fell+English&display=swap" rel="stylesheet">
    <style>
        body { 
            font-family: 'IM Fell English', serif;
            max-width: 800px;
            margin: 2rem auto;
            padding: 2rem;
            background: #0a0a0f;
            color: #c4c4c4;
            line-height: 1.6;
            background-image: 
                radial-gradient(circle at 50% 50%, rgba(29, 38, 54, 0.2), rgba(10, 10, 15, 0.4)),
                linear-gradient(rgba(10, 10, 15, 0.95), rgba(10, 10, 15, 0.95));
        }
        .location { 
            font-size: 2rem;
            color: #d4b16a;
            margin-bottom: 1.5rem;
            text-shadow: 0 0 10px rgba(212, 177, 106, 0.3);
            font-style: italic;
        }
        .description {
            font-size: 1.2rem;
            line-height: 1.8;
            margin-bottom: 2rem;
            color: #e0e0e0;
            text-shadow: 0 0 20px rgba(224, 224, 224, 0.1);
        }
        .inventory {
            background: rgba(20, 24, 32, 0.7);
            padding: 1.5rem;
            border-radius: 3px;
            margin-bottom: 2rem;
            border: 1px solid rgba(212, 177, 106, 0.2);
            box-shadow: 
                0 0 15px rgba(212, 177, 106, 0.1),
                inset 0 0 20px rgba(0, 0, 0, 0.4);
        }
        .inventory h3 {
            color: #d4b16a;
            margin-top: 0;
            font-style: italic;
            border-bottom: 1px solid rgba(212, 177, 106, 0.2);
            padding-bottom: 0.5rem;
        }
        .choices {
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }
        .choice-btn {
            padding: 1rem 1.5rem;
            background: rgba(20, 24, 32, 0.9);
            color: #d4b16a;
            border: 1px solid rgba(212, 177, 106, 0.3);
            border-radius: 2px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-family: 'IM Fell English', serif;
            font-size: 1.1rem;
            text-align: left;
            position: relative;
        }
        .choice-btn:hover {
            background: rgba(212, 177, 106, 0.1);
            border-color: rgba(212, 177, 106, 0.5);
            transform: translateX(10px);
            text-shadow: 0 0 5px rgba(212, 177, 106, 0.5);
        }
        .choice-btn::before {
            content: '»';
            position: absolute;
            right: 1rem;
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        .choice-btn:hover::before {
            opacity: 1;
        }
        .game-over {
            color: #ff4444;
            font-weight: bold;
            text-align: center;
            padding: 2rem;
            border: 1px solid rgba(255, 68, 68, 0.3);
            background: rgba(255, 68, 68, 0.1);
        }
        .game-over a {
            color: #d4b16a;
            text-decoration: none;
            border-bottom: 1px solid currentColor;
        }
        .game-over a:hover {
            color: #ff4444;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .description, .inventory, .choices {
            animation: fadeIn 0.8s ease-out forwards;
        }
        .loading-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.85);
            z-index: 1000;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        }
        
        .loading-text {
            color: #d4b16a;
            font-size: 1.5rem;
            margin-top: 2rem;
            font-style: italic;
            text-shadow: 0 0 10px rgba(212, 177, 106, 0.3);
            opacity: 0;
            animation: pulse 2s infinite;
        }
        
        .loading-symbol {
            width: 50px;
            height: 50px;
            border: 3px solid rgba(212, 177, 106, 0.3);
            border-radius: 50%;
            border-top-color: #d4b16a;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            to {
                transform: rotate(360deg);
            }
        }
        
        @keyframes pulse {
            0% { opacity: 0.3; }
            50% { opacity: 1; }
            100% { opacity: 0.3; }
        }
    </style>
</head>
<body>
    <div class="loading-overlay" id="loadingOverlay">
        <div class="loading-symbol"></div>
        <div class="loading-text">The forest whispers...</div>
    </div>
    
    <div class="location">{{ game_state.current_location }}</div>
    <div class="description">{{ game_state.description }}</div>
    
    <div class="inventory">
        <h3>Your Possessions</h3>
        <p>Vitality: {{ game_state.inventory.health }}</p>
        <p>Gold Pieces: {{ game_state.inventory.gold }}</p>
        <p>Carried Items: {{ ", ".join(game_state.inventory.items) if game_state.inventory.items else "Nothing but your courage" }}</p>
    </div>

    {% if not game_state.game_over %}
    <div class="choices">
        {% for choice in game_state.choices %}
        <form method="POST" action="/choose" onsubmit="showLoading()">
            <input type="hidden" name="choice" value="{{ choice }}">
            <button class="choice-btn" type="submit">{{ choice|safe }}</button>
        </form>
        {% endfor %}
    </div>
    {% else %}
    <div class="game-over">
        The tale ends here... but another awaits. <a href="/" onclick="showLoading()">Begin Anew</a>
    </div>
    {% endif %}

    <script>
        function showLoading() {
            document.getElementById('loadingOverlay').style.display = 'flex';
            // Disable all buttons to prevent double-submission
            document.querySelectorAll('button').forEach(button => {
                button.disabled = true;
            });
            return true;
        }
        
        // In case the user hits the back button, make sure the overlay is hidden
        window.onpageshow = function(event) {
            if (event.persisted) {
                document.getElementById('loadingOverlay').style.display = 'none';
                document.querySelectorAll('button').forEach(button => {
                    button.disabled = false;
                });
            }
        };
    </script>
</body>
</html>
"""

# Initialize game client with API key
print(os.getenv('GEMINI_API_KEY'))
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

def get_game_response(prompt: str, current_inventory: Inventory, story_history: List[str]) -> GameState:
    # Include story history in the prompt
    history_context = "\n".join(story_history) if story_history else "Game is starting"
    
    story_prompt = f"""You are running a fantasy text adventure game. Here's what has happened so far:

{history_context}

The player has the following inventory:
Health: {current_inventory.health}
Gold: {current_inventory.gold}
Items: {', '.join(current_inventory.items)}

Based on this choice: {prompt}

Respond with an engaging story moment and 2-4 choices for the player.
Format each choice on a new line starting with "A) ", "B) ", etc.
Make the choice text bold using <b> tags instead of asterisks.
Each choice should be followed by a short explanation in parentheses on a new line.

Example format:
[story text]

A) <b>First choice text</b>
(Explanation of first choice consequences)

B) <b>Second choice text</b>
(Explanation of second choice consequences)
"""
    
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=story_prompt
    )
    
    # Parse the response into GameState
    game_data = response.text
    
    # Split the response into description and choices
    parts = game_data.split('\n\n')
    description = parts[0]
    
    # Extract choices, removing the explanations in parentheses
    choices = [
        line.split(') ')[1].replace('<b>', '').replace('</b>', '').split('\n')[0]
        for line in parts[1:]
        if line.strip() and line[0] in 'ABC'
    ]
    
    # Add this moment to the story history
    story_history.append(f"Location: {session.get('current_location', 'Forest Path')}\n{description}\nChoice made: {prompt}")
    
    return GameState(
        current_location=session.get('current_location', "Forest Path"),
        description=description,
        choices=choices,
        inventory=current_inventory,
        game_over=False
    )

@app.route('/')
def home():
    # Initialize new game
    session['story_history'] = []
    session['current_location'] = "Forest Path"
    initial_inventory = Inventory(items=[], health=100, gold=10)
    initial_state = get_game_response("start game", initial_inventory, session['story_history'])
    return render_template_string(GAME_TEMPLATE, game_state=initial_state)

@app.route('/choose', methods=['POST'])
def choose():
    choice = request.form.get('choice')
    story_history = session.get('story_history', [])
    
    # Get current inventory from session or create new one
    current_inventory = Inventory(
        items=request.args.getlist('items[]'),
        health=int(request.args.get('health', 100)),
        gold=int(request.args.get('gold', 10))
    )
    
    game_state = get_game_response(choice, current_inventory, story_history)
    
    # Update session with new story history
    session['story_history'] = story_history
    session['current_location'] = game_state.current_location
    
    return render_template_string(GAME_TEMPLATE, game_state=game_state)

if __name__ == '__main__':
    app.run(debug=True)
