from typing import List, Tuple, Dict, Optional
from abc import ABC, abstractmethod
import time

# We'll import GridEnvironment only when needed to avoid circular imports
# from environment import GridEnvironment

class DeliveryAgent:
    def __init__(self, env):  # Remove type hint to avoid import issue
        self.env = env
        self.position = (0, 0)
        self.goal = (0, 0)
        self.fuel = 1000
        self.time_step = 0
        self.path: List[Tuple[int, int]] = []
        self.movement_history: List[Tuple[int, int, int]] = []
        
    def set_start_goal(self, start: Tuple[int, int], goal: Tuple[int, int]):
        self.position = start
        self.goal = goal
        self.movement_history = [(start[0], start[1], 0)]
        
    def move_to(self, new_position: Tuple[int, int]):
        cost = self.env.get_cost(new_position[0], new_position[1], self.time_step)
        self.fuel -= cost
        self.position = new_position
        self.time_step += 1
        self.movement_history.append((new_position[0], new_position[1], self.time_step))
        
    def replan(self, planner, recalculate_heuristic: bool = True) -> List[Tuple[int, int]]:
        self.path = planner.plan(self.position, self.goal, self.time_step, recalculate_heuristic)
        return self.path

class Planner(ABC):
    def __init__(self, env):
        self.env = env
        self.nodes_expanded = 0
        
    @abstractmethod
    def plan(self, start: Tuple[int, int], goal: Tuple[int, int], 
             start_time: int = 0, recalculate_heuristic: bool = True) -> List[Tuple[int, int]]:
        pass
        
    def get_neighbors(self, x: int, y: int, time_step: int = 0) -> List[Tuple[int, int, int]]:
        neighbors = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if self.env.is_valid_position(nx, ny, time_step):
                cost = self.env.get_cost(nx, ny, time_step)
                neighbors.append((nx, ny, cost))
        return neighbors

def calculate_path_cost(env, path: List[Tuple[int, int]], start_time: int = 0) -> int:
    total_cost = 0
    current_time = start_time
    for i in range(1, len(path)):
        x, y = path[i]
        total_cost += env.get_cost(x, y, current_time)
        current_time += 1
    return total_cost