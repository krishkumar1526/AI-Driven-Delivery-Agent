import argparse
import time
import json
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.environment import load_map_from_file
from src.agent import calculate_path_cost
from src.planners.uninformed import BFSPlanner, UniformCostPlanner
from src.planners.informed import AStarPlanner
from src.planners.local_search import HillClimbingPlanner, SimulatedAnnealingPlanner

# Custom JSON encoder to handle numpy types
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer, np.floating)):
            return int(obj) if isinstance(obj, np.integer) else float(obj)
        return super().default(obj)

def run_single_experiment(map_file: str, start: tuple, goal: tuple, 
                         planner_type: str, time_step: int = 0):
    env = load_map_from_file(map_file)
    
    planners = {
        'bfs': BFSPlanner(env),
        'uniform': UniformCostPlanner(env),
        'astar': AStarPlanner(env),
        'hillclimb': HillClimbingPlanner(env),
        'annealing': SimulatedAnnealingPlanner(env)
    }
    
    planner = planners[planner_type]
    
    start_time = time.time()
    path = planner.plan(start, goal, time_step)
    planning_time = time.time() - start_time
    
    total_cost = calculate_path_cost(env, path, time_step) if path else float('inf')
    
    result = {
        'planner': planner_type,
        'path_length': len(path) if path else 0,
        'path_cost': int(total_cost) if total_cost != float('inf') else 'inf',
        'nodes_expanded': int(planner.nodes_expanded),
        'planning_time': float(planning_time),
        'path_found': len(path) > 0
    }
    
    return result

def main():
    parser = argparse.ArgumentParser(description='Autonomous Delivery Agent')
    parser.add_argument('--map', type=str, required=True, help='Map file')
    parser.add_argument('--start', type=str, required=True, help='Start position (x,y)')
    parser.add_argument('--goal', type=str, required=True, help='Goal position (x,y)')
    parser.add_argument('--planner', type=str, 
                       choices=['bfs', 'uniform', 'astar', 'hillclimb', 'annealing'],
                       required=True, help='Planning algorithm')
    parser.add_argument('--time', type=int, default=0, help='Start time step')
    
    args = parser.parse_args()
    
    start = tuple(map(int, args.start.split(',')))
    goal = tuple(map(int, args.goal.split(',')))
    
    result = run_single_experiment(args.map, start, goal, args.planner, args.time)
    print(json.dumps(result, indent=2, cls=NumpyEncoder))

if __name__ == '__main__':
    main()