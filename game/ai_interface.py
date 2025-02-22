from google import genai
from pydantic import BaseModel
from .models import GameState, Inventory
from typing import List
import os

class Choice(BaseModel):
    text: str
    explanation: str

class StoryResponse(BaseModel):
    description: str
    choices: List[Choice]

class AIGameManager:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
    
    def get_story_response(self, prompt: str, current_inventory: Inventory, story_history: List[str]) -> StoryResponse:
        # Format the context for the AI
        history_context = "\n".join(story_history) if story_history else "Game is starting"
        
        story_prompt = f"""You are running a fantasy text adventure game. Here's what has happened so far:

{history_context}

The player has the following inventory:
Health: {current_inventory.health}
Gold: {current_inventory.gold}
Items: {', '.join(current_inventory.items)}

Based on this choice: {prompt}

Respond with an engaging story moment and 2-4 choices for the player."""

        response = self.client.models.generate_content(
            model='gemini-2.0-flash',
            contents=story_prompt,
            config={
                'response_mime_type': 'application/json',
                'response_schema': StoryResponse,
            }
        )

        # The response will automatically be parsed into a StoryResponse object
        return response.parsed

    def parse_response(self, response: StoryResponse) -> tuple[str, List[str]]:
        # Extract just the choice text for backwards compatibility
        description = response.description
        choices = [choice.text for choice in response.choices]
        
        return description, choices 