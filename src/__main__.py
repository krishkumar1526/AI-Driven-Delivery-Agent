"""
Main entry point for the autonomous delivery agent
"""

import sys
import os

# Add the parent directory to path so we can import other modules
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from environment import GridEnvironment, load_map_from_file
from agent import calculate_path_cost
from planners.uninformed import BFSPlanner, UniformCostPlanner
from planners.informed import AStarPlanner

def main():
    """Main function"""
    print("Autonomous Delivery Agent - Path Planning System")
    print("=" * 50)
    
    # Test basic functionality
    env = load_map_from_file('../maps/small.map')
    print(f"Map loaded: {env.width}x{env.height}")
    
    # Test different planners
    planners = [
        ("BFS", BFSPlanner(env)),
        ("Uniform Cost", UniformCostPlanner(env)),
        ("A*", AStarPlanner(env)),
    ]
    
    for name, planner in planners:
        path = planner.plan((0, 0), (4, 4))
        if path:
            cost = calculate_path_cost(env, path)
            print(f"{name}: Path found! Steps: {len(path)}, Cost: {cost}")
        else:
            print(f"{name}: No path found")

if __name__ == '__main__':
    main()