from flask import Flask, request, render_template
from dotenv import load_dotenv
from game.models import Inventory
from game.game_logic import GameManager
import os

# Load environment variables (e.g., API keys)
load_dotenv()

# Initialize Flask app and game manager
app = Flask(__name__)
# Simple secret key for development - should be changed in production
app.secret_key = 'dev'
game_manager = GameManager()

@app.route('/')
def home():
    """
    Homepage route - starts a new game
    Returns: Rendered game template with initial game state
    """
    game_state = game_manager.initialize_game()
    return render_template('game.html', game_state=game_state)

@app.route('/choose', methods=['POST'])
def choose():
    """
    Handles player choices and advances the game state
    
    Gets the player's choice from form data, reconstructs current inventory
    from URL parameters, and processes the turn to get the new game state
    
    Returns: Rendered game template with updated game state
    """
    choice = request.form.get('choice')
    
    # Reconstruct current inventory from URL parameters
    current_inventory = Inventory(
        items=request.args.getlist('items[]'),
        health=int(request.args.get('health', 100)),
        gold=int(request.args.get('gold', 10))
    )
    
    # Process the turn and render the updated game state
    game_state = game_manager.process_turn(choice, current_inventory)
    return render_template('game.html', game_state=game_state)

if __name__ == '__main__':
    # Run the Flask development server
    app.run(host='0.0.0.0', debug=True, port=8080)
