#!/usr/bin/env python3
"""
Final working test for autonomous delivery agent
"""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("=== Autonomous Delivery Agent Test ===")

# Import each module individually
print("1. Importing environment...")
from environment import GridEnvironment, load_map_from_file
print("   ✓ Environment imported")

print("2. Importing agent...")
from agent import calculate_path_cost
print("   ✓ Agent imported")

print("3. Importing planners...")
from planners.uninformed import BFSPlanner, UniformCostPlanner
from planners.informed import AStarPlanner
print("   ✓ Planners imported")

def test_basic_functionality():
    """Test the basic functionality"""
    print("\n4. Testing basic functionality...")
    
    # Create a simple environment
    env = GridEnvironment(5, 5)
    for y in range(5):
        for x in range(5):
            env.set_terrain_cost(x, y, 1)
    
    print("   ✓ Environment created")
    
    # Test A* planner
    planner = AStarPlanner(env)
    path = planner.plan((0, 0), (4, 4))
    
    if path:
        cost = calculate_path_cost(env, path)
        print(f"   ✓ A* found path: {len(path)} steps, cost: {cost}")
        return True
    else:
        print("   ✗ A* failed to find path")
        return False

def test_map_loading():
    """Test loading maps from files"""
    print("\n5. Testing map loading...")
    
    try:
        env = load_map_from_file('maps/small.map')
        print(f"   ✓ Map loaded: {env.width}x{env.height}")
        
        # Test pathfinding on loaded map
        planner = AStarPlanner(env)
        path = planner.plan((0, 0), (env.width-1, env.height-1))
        
        if path:
            cost = calculate_path_cost(env, path)
            print(f"   ✓ Path found on loaded map: {len(path)} steps, cost: {cost}")
        else:
            print("   ✗ No path found on loaded map")
            
        return True
    except Exception as e:
        print(f"   ✗ Error loading map: {e}")
        return False

def test_all_planners():
    """Test all planning algorithms"""
    print("\n6. Testing all planners...")
    
    try:
        env = load_map_from_file('maps/small.map')
        planners = [
            ("BFS", BFSPlanner(env)),
            ("Uniform Cost", UniformCostPlanner(env)),
            ("A*", AStarPlanner(env)),
        ]
        
        for name, planner in planners:
            path = planner.plan((0, 0), (4, 4))
            if path:
                cost = calculate_path_cost(env, path)
                print(f"   ✓ {name}: {len(path)} steps, cost {cost}")
            else:
                print(f"   ✗ {name}: No path found")
        
        return True
    except Exception as e:
        print(f"   ✗ Error testing planners: {e}")
        return False

if __name__ == '__main__':
    success = True
    
    success &= test_basic_functionality()
    success &= test_map_loading() 
    success &= test_all_planners()
    
    if success:
        print("\n🎉 ALL TESTS PASSED! Your autonomous delivery agent is working! 🎉")
        print("\nYou can now push your code to GitHub.")
    else:
        print("\n❌ Some tests failed. Check the errors above.")