from flask import session
from .models import GameState, Inventory
from .ai_interface import AIGameManager

class GameManager:
    """Manages the core game logic and state transitions"""
    
    def __init__(self):
        # Initialize the AI component that generates story responses
        self.ai_manager = AIGameManager()

    def initialize_game(self) -> GameState:
        """
        Sets up a new game session with initial values
        Returns: Initial GameState with starting location and inventory
        """
        # Clear any existing story history
        session['story_history'] = []
        session['current_location'] = "Forest Path"
        
        # Create starting inventory with basic items/stats
        initial_inventory = Inventory(items=[], health=100, gold=10)
        return self.process_turn("start game", initial_inventory)

    def process_turn(self, choice: str, current_inventory: Inventory) -> GameState:
        """
        Handles a single turn/choice in the game
        
        Args:
            choice: The player's selected action
            current_inventory: Current state of player's inventory
            
        Returns:
            GameState object containing the new game state after the choice
        """
        # Get or initialize story history from session
        story_history = session.get('story_history', [])
        
        # Get AI-generated response based on player's choice
        response = self.ai_manager.get_story_response(choice, current_inventory, story_history)
        description, choices = self.ai_manager.parse_response(response)
        
        # Add the latest story beat to history
        story_history.append(
            f"Location: {session.get('current_location', 'Forest Path')}\n{description}\nChoice made: {choice}"
        )
        session['story_history'] = story_history
        
        # Return new game state
        return GameState(
            current_location=session.get('current_location', "Forest Path"),
            description=description,
            choices=choices,
            inventory=current_inventory,
            game_over=False
        ) 