#!/usr/bin/env python3
"""
Main experiment runner for comparing path planning algorithms
"""

import json
import time
import numpy as np
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Now import from src
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

def run_comprehensive_experiments():
    """Run all algorithms on all test maps"""
    results = {}
    maps = ['small.map', 'medium.map']
    algorithms = {
        'bfs': BFSPlanner,
        'uniform_cost': UniformCostPlanner,
        'astar': AStarPlanner,
        'hill_climbing': HillClimbingPlanner,
        'simulated_annealing': SimulatedAnnealingPlanner
    }
    
    for map_name in maps:
        print(f"\n=== Testing on {map_name} ===")
        results[map_name] = {}
        
        try:
            env = load_map_from_file(f'maps/{map_name}')
            print(f"Map loaded: {env.width}x{env.height}")
            
            for algo_name, algo_class in algorithms.items():
                print(f"Running {algo_name}...")
                
                planner = algo_class(env)
                start_time = time.time()
                
                path = planner.plan((0, 0), (env.width-1, env.height-1))
                planning_time = time.time() - start_time
                
                total_cost = calculate_path_cost(env, path) if path else float('inf')
                
                results[map_name][algo_name] = {
                    'path_length': len(path) if path else 0,
                    'path_cost': int(total_cost) if total_cost != float('inf') else 'inf',
                    'nodes_expanded': int(planner.nodes_expanded),
                    'planning_time': float(planning_time),
                    'success': len(path) > 0 if path else False
                }
                print(f"  {algo_name}: Path found: {len(path) > 0}, Cost: {total_cost}")
                
        except Exception as e:
            print(f"Error with {map_name}: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    with open('results/experiment_results.json', 'w') as f:
        json.dump(results, f, indent=2, cls=NumpyEncoder)
    
    print("\nExperiments completed! Results saved to results/experiment_results.json")

if __name__ == '__main__':
    run_comprehensive_experiments()