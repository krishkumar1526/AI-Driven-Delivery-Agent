import numpy as np
from enum import Enum
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass

class CellType(Enum):
    ROAD = 1
    GRASS = 3
    WATER = 10
    MOUNTAIN = 15
    OBSTACLE = 999

@dataclass
class MovingObstacle:
    positions: List[Tuple[int, int]]
    current_step: int = 0
    
    def get_position_at_time(self, time_step: int) -> Tuple[int, int]:
        return self.positions[time_step % len(self.positions)]

class GridEnvironment:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = np.ones((height, width), dtype=int)
        self.static_obstacles = set()
        self.moving_obstacles: List[MovingObstacle] = []
        self.dynamic_changes: Dict[int, List[Tuple[int, int, int]]] = {}
        
    def set_terrain_cost(self, x: int, y: int, cost: int):
        self.grid[y, x] = cost
        
    def add_static_obstacle(self, x: int, y: int):
        self.static_obstacles.add((x, y))
        
    def add_moving_obstacle(self, positions: List[Tuple[int, int]]):
        self.moving_obstacles.append(MovingObstacle(positions))
        
    def add_dynamic_change(self, time_step: int, x: int, y: int, new_cost: int):
        if time_step not in self.dynamic_changes:
            self.dynamic_changes[time_step] = []
        self.dynamic_changes[time_step].append((x, y, new_cost))
        
    def get_cost(self, x: int, y: int, time_step: int = 0) -> int:
        if (x, y) in self.static_obstacles:
            return 9999
            
        if time_step in self.dynamic_changes:
            for dx, dy, new_cost in self.dynamic_changes[time_step]:
                if dx == x and dy == y:
                    return new_cost
        
        for obstacle in self.moving_obstacles:
            if obstacle.get_position_at_time(time_step) == (x, y):
                return 9999
                
        return self.grid[y, x]
    
    def is_valid_position(self, x: int, y: int, time_step: int = 0) -> bool:
        return (0 <= x < self.width and 0 <= y < self.height and 
                self.get_cost(x, y, time_step) < 9999)

def load_map_from_file(filename: str) -> GridEnvironment:
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    if not lines:
        raise ValueError("Map file is empty")
    
    width, height = map(int, lines[0].split())
    env = GridEnvironment(width, height)
    
    for y in range(height):
        if y + 1 >= len(lines):
            break
        row = list(map(int, lines[1+y].split()))
        for x in range(min(width, len(row))):
            env.set_terrain_cost(x, y, row[x])
    
    return env