import random
import math
from typing import List, Tuple
from agent import Planner

class HillClimbingPlanner(Planner):
    def __init__(self, env, max_restarts=10, max_iterations=1000):
        super().__init__(env)
        self.max_restarts = max_restarts
        self.max_iterations = max_iterations
        
    def evaluate_path(self, path: List[Tuple[int, int]], start_time: int) -> int:
        total_cost = 0
        current_time = start_time
        
        for i in range(1, len(path)):
            x, y = path[i]
            if not self.env.is_valid_position(x, y, current_time):
                return float('inf')
            total_cost += self.env.get_cost(x, y, current_time)
            current_time += 1
            
        return total_cost
    
    def generate_random_path(self, start: Tuple[int, int], goal: Tuple[int, int], 
                           max_length: int = 50) -> List[Tuple[int, int]]:
        path = [start]
        current = start
        visited = set([start])
        
        for _ in range(max_length):
            if current == goal:
                break
                
            neighbors = self.get_neighbors(current[0], current[1], 0)
            valid_neighbors = [(nx, ny) for nx, ny, cost in neighbors 
                             if (nx, ny) not in visited]
            
            if not valid_neighbors:
                break
                
            next_cell = random.choice(valid_neighbors)
            path.append(next_cell)
            visited.add(next_cell)
            current = next_cell
            
        return path
    
    def mutate_path(self, path: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        if len(path) <= 2:
            return path
            
        i = random.randint(0, len(path) - 2)
        j = random.randint(i + 1, len(path) - 1)
        
        new_segment = self.generate_random_path(path[i], path[j], j - i + 5)
        
        if len(new_segment) > 1:
            return path[:i] + new_segment + path[j+1:]
        return path
    
    def plan(self, start: Tuple[int, int], goal: Tuple[int, int], 
             start_time: int = 0, recalculate_heuristic: bool = True) -> List[Tuple[int, int]]:
        self.nodes_expanded = 0
        best_path = None
        best_cost = float('inf')
        
        for restart in range(self.max_restarts):
            current_path = self.generate_random_path(start, goal)
            current_cost = self.evaluate_path(current_path, start_time)
            
            for iteration in range(self.max_iterations):
                self.nodes_expanded += 1
                
                new_path = self.mutate_path(current_path)
                new_cost = self.evaluate_path(new_path, start_time)
                
                if new_cost < current_cost:
                    current_path, current_cost = new_path, new_cost
                    
                    if new_cost < best_cost:
                        best_path, best_cost = new_path, new_cost
                        
                if random.random() < 0.1:
                    break
                    
        return best_path if best_path else []

class SimulatedAnnealingPlanner(HillClimbingPlanner):
    def __init__(self, env, initial_temp=1000, cooling_rate=0.95, max_iterations=1000):
        super().__init__(env, max_restarts=1, max_iterations=max_iterations)
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        
    def plan(self, start: Tuple[int, int], goal: Tuple[int, int], 
             start_time: int = 0, recalculate_heuristic: bool = True) -> List[Tuple[int, int]]:
        self.nodes_expanded = 0
        
        current_path = self.generate_random_path(start, goal)
        current_cost = self.evaluate_path(current_path, start_time)
        best_path, best_cost = current_path, current_cost
        
        temperature = self.initial_temp
        
        for iteration in range(self.max_iterations):
            self.nodes_expanded += 1
            
            new_path = self.mutate_path(current_path)
            new_cost = self.evaluate_path(new_path, start_time)
            
            if new_cost < current_cost:
                current_path, current_cost = new_path, new_cost
                if new_cost < best_cost:
                    best_path, best_cost = new_path, new_cost
            else:
                delta = new_cost - current_cost
                acceptance_prob = math.exp(-delta / temperature)
                
                if random.random() < acceptance_prob:
                    current_path, current_cost = new_path, new_cost
            
            temperature *= self.cooling_rate
            
            if temperature < 1e-6:
                break
                
        return best_path