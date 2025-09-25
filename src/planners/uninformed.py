from collections import deque, defaultdict
import heapq
from typing import List, Tuple, Dict
from agent import Planner

class BFSPlanner(Planner):
    def plan(self, start: Tuple[int, int], goal: Tuple[int, int], 
             start_time: int = 0, recalculate_heuristic: bool = True) -> List[Tuple[int, int]]:
        self.nodes_expanded = 0
        queue = deque([(start[0], start[1], start_time, [start])])
        visited = set()
        
        while queue:
            x, y, time_step, path = queue.popleft()
            
            if (x, y) == goal:
                return path
                
            if (x, y, time_step) in visited:
                continue
            visited.add((x, y, time_step))
            self.nodes_expanded += 1
            
            for nx, ny, cost in self.get_neighbors(x, y, time_step):
                if (nx, ny, time_step + 1) not in visited:
                    new_path = path + [(nx, ny)]
                    queue.append((nx, ny, time_step + 1, new_path))
                    
        return []

class UniformCostPlanner(Planner):
    def plan(self, start: Tuple[int, int], goal: Tuple[int, int], 
             start_time: int = 0, recalculate_heuristic: bool = True) -> List[Tuple[int, int]]:
        self.nodes_expanded = 0
        queue = [(0, start[0], start[1], start_time, [start])]
        visited = defaultdict(lambda: float('inf'))
        
        while queue:
            total_cost, x, y, time_step, path = heapq.heappop(queue)
            
            if (x, y) == goal:
                return path
                
            if total_cost >= visited[(x, y, time_step)]:
                continue
            visited[(x, y, time_step)] = total_cost
            self.nodes_expanded += 1
            
            for nx, ny, cost in self.get_neighbors(x, y, time_step):
                new_cost = total_cost + cost
                if new_cost < visited[(nx, ny, time_step + 1)]:
                    new_path = path + [(nx, ny)]
                    heapq.heappush(queue, (new_cost, nx, ny, time_step + 1, new_path))
                    
        return []