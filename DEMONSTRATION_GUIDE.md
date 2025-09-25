Project Demonstration Guide

Autonomous Delivery Agent - Live Demo Instructions



1\. Quick Start Demonstration



1.1 Basic Functionality Test



&nbsp;Test A\* algorithm on small map

python src/cli.py --map maps/small.map --start 0,0 --goal 4,4 --planner astar



&nbsp;Expected Output:

{

&nbsp;   "planner": "astar",

&nbsp;   "path\_length": 9,

&nbsp;   "path\_cost": 8,

&nbsp;   "nodes\_expanded": 15,

&nbsp;   "planning\_time": 0.0003,

&nbsp;   "path\_found": true

}



1.2 Algorithm Comparison



Compare all algorithms on same map:



python src/cli.py --map maps/small.map --start 0,0 --goal 4,4 --planner bfs

python src/cli.py --map maps/small.map --start 0,0 --goal 4,4 --planner uniform

python src/cli.py --map maps/small.map --start 0,0 --goal 4,4 --planner astar





2\. Demo Scenarios



2.1 Scenario 1: Basic Pathfinding



Objective: Demonstrate optimal path finding:



python src/cli.py --map maps/small.map --start 0,0 --goal 4,4 --planner astar



Expected Results:



Path found: (0,0) → (4,4)



Cost: 8 units



Steps: 9 moves



Time: < 1ms





2.2 Scenario 2: Terrain Cost Awareness



Objective: Show cost-sensitive planning:



python src/cli.py --map maps/medium.map --start 0,0 --goal 9,9 --planner uniform



Key Point: Uniform-cost avoids high-cost terrain even if path is longer.





2.3 Scenario 3: Dynamic Replanning



Objective: Demonstrate obstacle avoidance:



Simulate dynamic obstacle scenario



python demos/dynamic\_demo.py







3\. Live Demonstration Script





3.1 Introduction (2 minutes)



Project overview and objectives:



Key algorithms implemented



Real-world applications





3.2 Technical Demo (3 minutes)



Step 1: Show environment loading:



python -c "from src.environment import load\_map\_from\_file; env = load\_map\_from\_file('maps/small.map'); print(f'Map loaded: {env.width}x{env.height}')"



Step 2: Demonstrate A\* algorithm

python src/cli.py --map maps/small.map --start 0,0 --goal 4,4 --planner astar



Step 3: Compare with BFS

python src/cli.py --map maps/small.map --start 0,0 --goal 4,4 --planner bfs



Step 4: Show terrain cost handling

python src/cli.py --map maps/medium.map --start 0,0 --goal 9,9 --planner uniform





3.3 Results Analysis (2 minutes)



Display performance comparison table:



Discuss algorithm trade-offs



Show dynamic replanning capability





4\. Expected Output Examples



4.1 Successful Path Finding

{

&nbsp;   "planner": "astar",

&nbsp;   "path\_length": 9,

&nbsp;   "path\_cost": 8,

&nbsp;   "nodes\_expanded": 15,

&nbsp;   "planning\_time": 0.0003,

&nbsp;   "path\_found": true

}





4.2 No Path Available

{

&nbsp;   "planner": "bfs",

&nbsp;   "path\_length": 0,

&nbsp;   "path\_cost": "inf",

&nbsp;   "nodes\_expanded": 42,

&nbsp;   "planning\_time": 0.0012,

&nbsp;   "path\_found": false

}







5\. Troubleshooting



5.1 Common Issues



Module not found: Run from project root directory



Map file error: Check map file path and format



Import errors: Ensure Python path includes src directory





5.2 Verification Commands



Verify installation:



python -c "from src.environment import GridEnvironment; print('✓ Environment OK')"





Test basic functionality:



python final\_test.py





Run comprehensive tests:



python run\_experiments.py







6\. Demonstration Tips



6.1 For Academic Presentation



Focus on algorithm comparisons



Highlight A\* efficiency gains



Demonstrate dynamic replanning



Discuss real-world applications





6.2 For Technical Audience



Show code architecture



Explain heuristic design



Discuss complexity analysis



Demonstrate extensibility







7\. Success Metrics



A successful demonstration should show:



✅ All algorithms finding valid paths



✅ Clear performance differences between algorithms



✅ Proper handling of terrain costs



✅ Effective dynamic replanning



✅ Professional command-line interface







8\. Conclusion



This demonstration showcases a complete AI pathfinding system that:



Implements classical search algorithms



Provides practical path planning capabilities



Offers insights into algorithm performance



Serves as a foundation for advanced AI projects





