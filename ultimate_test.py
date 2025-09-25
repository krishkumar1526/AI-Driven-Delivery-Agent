#!/usr/bin/env python3
"""
Ultimate simple test - import each file directly
"""

print("Testing autonomous delivery agent...")

# Test 1: Environment
print("1. Testing environment...")
exec(open("src/environment.py").read())
print("   ✓ Environment OK")

# Test 2: Agent
print("2. Testing agent...")
exec(open("src/agent.py").read())
print("   ✓ Agent OK")

# Test 3: Test basic functionality
print("3. Testing basic path planning...")

# Create a simple environment
env = GridEnvironment(5, 5)
for y in range(5):
    for x in range(5):
        env.set_terrain_cost(x, y, 1)

# Test A* planner
planner = AStarPlanner(env)
path = planner.plan((0, 0), (4, 4))

if path:
    print(f"   ✓ Path found! Steps: {len(path)}")
else:
    print("   ✗ No path found")

print("=== Test completed ===")