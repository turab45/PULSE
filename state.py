from typing import TypedDict

class BatsmanState(TypedDict):
    runs: int
    balls: int
    fours: int
    sixes: int
    
    strike_rate: float
    boundary_per_ball: float
    boundary_percentage: float
    summary: str
