import heapq
from typing import List, Tuple, Dict
from agent import Planner

class AStarPlanner(Planner):
    def heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def plan(self, start: Tuple[int, int], goal: Tuple[int, int], 
             start_time: int = 0, recalculate_heuristic: bool = True) -> List[Tuple[int, int]]:
        self.nodes_expanded = 0
        queue = [(self.heuristic(start, goal), 0, start[0], start[1], start_time, [start])]
        visited = {}
        
        while queue:
            f_cost, g_cost, x, y, time_step, path = heapq.heappop(queue)
            
            if (x, y) == goal:
                return path
                
            state = (x, y, time_step)
            if state in visited and visited[state] <= g_cost:
                continue
            visited[state] = g_cost
            self.nodes_expanded += 1
            
            for nx, ny, cost in self.get_neighbors(x, y, time_step):
                new_g_cost = g_cost + cost
                new_f_cost = new_g_cost + self.heuristic((nx, ny), goal)
                new_state = (nx, ny, time_step + 1)
                
                if new_state not in visited or new_g_cost < visited[new_state]:
                    new_path = path + [(nx, ny)]
                    heapq.heappush(queue, (new_f_cost, new_g_cost, nx, ny, time_step + 1, new_path))
                    
        return []