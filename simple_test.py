#!/usr/bin/env python3
"""
Simple test file to verify all components work
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Now import using absolute paths
try:
    from src.environment import GridEnvironment, load_map_from_file
    from src.agent import calculate_path_cost
    from src.planners.uninformed import BFSPlanner, UniformCostPlanner
    from src.planners.informed import AStarPlanner
    print("✓ All imports successful!")
except ImportError as e:
    print(f"Import error: {e}")
    print("Trying alternative import method...")
    
    # Alternative: Import directly from files
    import importlib.util
    
    # Import environment
    spec = importlib.util.spec_from_file_location("environment", "src/environment.py")
    environment = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(environment)
    GridEnvironment = environment.GridEnvironment
    load_map_from_file = environment.load_map_from_file
    
    # Import agent
    spec = importlib.util.spec_from_file_location("agent", "src/agent.py")
    agent = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(agent)
    calculate_path_cost = agent.calculate_path_cost
    
    # Import planners
    spec = importlib.util.spec_from_file_location("uninformed", "src/planners/uninformed.py")
    uninformed = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(uninformed)
    BFSPlanner = uninformed.BFSPlanner
    UniformCostPlanner = uninformed.UniformCostPlanner
    
    spec = importlib.util.spec_from_file_location("informed", "src/planners/informed.py")
    informed = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(informed)
    AStarPlanner = informed.AStarPlanner

def test_basic_functionality():
    """Test basic functionality"""
    print("=== Testing Basic Functionality ===")
    
    # Test 1: Create environment
    print("1. Creating environment...")
    try:
        env = GridEnvironment(5, 5)
        print("   ✓ Environment created")
    except Exception as e:
        print(f"   ✗ Error creating environment: {e}")
        return False
    
    # Test 2: Load map from file
    print("2. Loading map from file...")
    try:
        env = load_map_from_file('maps/small.map')
        print("   ✓ Map loaded successfully")
    except Exception as e:
        print(f"   ✗ Error loading map: {e}")
        return False
    
    # Test 3: Test A* planner
    print("3. Testing A* planner...")
    try:
        planner = AStarPlanner(env)
        path = planner.plan((0, 0), (4, 4))
        cost = calculate_path_cost(env, path) if path else "No path"
        print(f"   ✓ A* found path: {len(path)} steps, cost: {cost}")
    except Exception as e:
        print(f"   ✗ Error with A*: {e}")
        return False
    
    print("=== All tests passed! ===")
    return True

if __name__ == '__main__':
    test_basic_functionality()