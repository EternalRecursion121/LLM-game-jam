from pydantic import BaseModel
from typing import List

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