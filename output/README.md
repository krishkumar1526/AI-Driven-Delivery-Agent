Output Generator - Autonomous Delivery Agent



This folder contains comprehensive output generators for the Autonomous Delivery Agent project.



📁 Folder Structure



output/

├── output\_generator.py # Main output generator class

├── run\_output\_generator.py # User-friendly runner script

├── test\_output.py # Test script

├── README.md # This file

├── results/ # JSON results files

├── reports/ # Text reports

├── visualizations/ # Charts and graphs (future)

├── logs/ # Execution logs

└── examples/ # Example configurations





🚀 Quick Start



Basic Usage



Generate outputs for small map

python run\_output\_generator.py --maps ../maps/small.map --start 0,0 --goal 4,4



Generate outputs for multiple maps

python run\_output\_generator.py --maps ../maps/small.map ../maps/medium.map --start 0,0 --goal 9,9





Using the Generator Programmatically



from output\_generator import OutputGenerator



generator = OutputGenerator("my\_outputs")

results = generator.generate\_all\_outputs(

    maps=\["../maps/small.map"],

    start=(0, 0),

    goal=(4, 4)

)





📊 Generated Outputs

The system generates these files automatically:



1\. JSON Results (results/detailed\_results.json)

Detailed algorithm performance data



Machine-readable format



Complete experiment results



2\. Text Reports (reports/performance\_report.txt)

Human-readable performance summary



Algorithm comparison tables



Executive recommendations



3\. Executive Summary (reports/executive\_summary.txt)

High-level project summary



Success metrics



Key findings



4\. Execution Logs (logs/execution\_log.txt)

Detailed execution timeline



Error tracking



Performance metrics



⚙️ Configuration

You can customize:



Maps: Any valid map file



Positions: Any start/goal coordinates



Algorithms: All 5 planning algorithms



Output formats: JSON, text, summary, logs



🧪 Testing



\# Run basic test

python test\_output.py



\# Test specific scenarios

python run\_output\_generator.py --maps ../maps/small.map --start 1,1 --goal 3,3





📈 Output Examples

See the examples/ folder for sample configurations and expected outputs.



🆘 Troubleshooting

Map not found: Ensure correct relative paths to map files



Import errors: Run from project root directory



No output: Check that maps and positions are valid





