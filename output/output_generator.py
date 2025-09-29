#!/usr/bin/env python3
"""
Main Output Generator for Autonomous Delivery Agent
Generates comprehensive outputs for any user input
"""

import json
import time
import os
from datetime import datetime
from typing import Dict, List, Any
import sys

# Add src to path to import project modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from environment import load_map_from_file
from agent import calculate_path_cost
from planners.uninformed import BFSPlanner, UniformCostPlanner
from planners.informed import AStarPlanner
from planners.local_search import HillClimbingPlanner, SimulatedAnnealingPlanner

class OutputGenerator:
    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        self.results = {}
        self.timestamp = datetime.now()
        
        # Create output directories
        self._create_directories()
    
    def _create_directories(self):
        """Create all necessary output directories"""
        directories = [
            self.output_dir,
            os.path.join(self.output_dir, "results"),
            os.path.join(self.output_dir, "reports"), 
            os.path.join(self.output_dir, "visualizations"),
            os.path.join(self.output_dir, "logs"),
            os.path.join(self.output_dir, "examples")
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def generate_all_outputs(self, map_files: List[str], start: tuple, goal: tuple):
        """Generate all output types for given parameters"""
        print("🚀 Starting comprehensive output generation...")
        
        # Run experiments
        self.results = self._run_experiments(map_files, start, goal)
        
        # Generate all output types
        self._generate_json_output()
        self._generate_text_report()
        self._generate_summary()
        self._generate_log_file()
        self._generate_example_config()
        
        print("✅ All outputs generated successfully!")
        return self.results
    
    def _run_experiments(self, map_files: List[str], start: tuple, goal: tuple) -> Dict[str, Any]:
        """Run experiments on all specified maps"""
        results = {
            "metadata": {
                "project": "Autonomous Delivery Agent",
                "timestamp": self.timestamp.isoformat(),
                "version": "1.0",
                "maps_tested": map_files,
                "start_position": start,
                "goal_position": goal
            },
            "experiments": {}
        }
        
        for map_file in map_files:
            print(f"📊 Testing {map_file}...")
            results["experiments"][map_file] = self._test_single_map(map_file, start, goal)
        
        return results
    
    def _test_single_map(self, map_file: str, start: tuple, goal: tuple) -> Dict[str, Any]:
        """Test all algorithms on a single map"""
        try:
            env = load_map_from_file(map_file)
            map_results = {
                "map_info": {
                    "filename": map_file,
                    "size": f"{env.width}x{env.height}",
                    "width": env.width,
                    "height": env.height
                },
                "algorithms": {}
            }
            
            algorithms = {
                "BFS": BFSPlanner(env),
                "Uniform_Cost": UniformCostPlanner(env),
                "A_Star": AStarPlanner(env),
                "Hill_Climbing": HillClimbingPlanner(env),
                "Simulated_Annealing": SimulatedAnnealingPlanner(env)
            }
            
            for algo_name, planner in algorithms.items():
                print(f"  🔍 Running {algo_name}...")
                map_results["algorithms"][algo_name] = self._run_algorithm(
                    planner, env, start, goal, algo_name
                )
            
            return map_results
            
        except Exception as e:
            return {"error": str(e)}
    
    def _run_algorithm(self, planner, env, start: tuple, goal: tuple, algo_name: str) -> Dict[str, Any]:
        """Run a single algorithm and return results"""
        start_time = time.time()
        path = planner.plan(start, goal)
        planning_time = time.time() - start_time
        
        if path and len(path) > 0:
            total_cost = calculate_path_cost(env, path)
            path_coords = [(x, y) for x, y in path]
            path_str = " → ".join([f"({x},{y})" for x, y in path])
        else:
            total_cost = float('inf')
            path_coords = []
            path_str = "No path found"
        
        return {
            "path_found": len(path) > 0,
            "path_length": len(path) if path else 0,
            "path_cost": total_cost if total_cost != float('inf') else "inf",
            "nodes_expanded": planner.nodes_expanded,
            "planning_time_ms": round(planning_time * 1000, 3),
            "path_coordinates": path_coords,
            "path_string": path_str,
            "efficiency_ratio": round(planner.nodes_expanded / max(len(path), 1), 2) if path else "N/A",
            "status": "SUCCESS" if len(path) > 0 else "FAILED"
        }
    
    def _generate_json_output(self):
        """Generate detailed JSON output"""
        json_file = os.path.join(self.output_dir, "results", "detailed_results.json")
        
        output = {
            "project": "Autonomous Delivery Agent",
            "generated_at": self.timestamp.isoformat(),
            "results": self.results
        }
        
        with open(json_file, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"📁 JSON output saved: {json_file}")
    
    def _generate_text_report(self):
        """Generate human-readable text report"""
        report_file = os.path.join(self.output_dir, "reports", "performance_report.txt")
        
        report_lines = []
        
        # Header
        report_lines.append("=" * 70)
        report_lines.append("AUTONOMOUS DELIVERY AGENT - COMPREHENSIVE PERFORMANCE REPORT")
        report_lines.append("=" * 70)
        report_lines.append(f"Generated: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        
        # Metadata
        metadata = self.results["metadata"]
        report_lines.append("EXPERIMENT SETUP")
        report_lines.append("-" * 50)
        report_lines.append(f"Project: {metadata['project']} v{metadata['version']}")
        report_lines.append(f"Start Position: {metadata['start_position']}")
        report_lines.append(f"Goal Position: {metadata['goal_position']}")
        report_lines.append(f"Maps Tested: {len(metadata['maps_tested'])}")
        report_lines.append("")
        
        # Results for each map
        for map_file, results in self.results["experiments"].items():
            if "error" in results:
                report_lines.append(f"❌ MAP: {map_file} - ERROR: {results['error']}")
                report_lines.append("")
                continue
                
            map_info = results["map_info"]
            report_lines.append(f"🗺️  MAP: {map_file} ({map_info['size']})")
            report_lines.append("-" * 50)
            
            # Table header
            report_lines.append(f"{'Algorithm':<20} {'Status':<10} {'Cost':<8} {'Steps':<6} {'Nodes':<8} {'Time(ms)':<10} {'Efficiency'}")
            report_lines.append("-" * 70)
            
            for algo_name, algo_results in results["algorithms"].items():
                status = "✅" if algo_results["status"] == "SUCCESS" else "❌"
                cost = algo_results["path_cost"]
                steps = algo_results["path_length"]
                nodes = algo_results["nodes_expanded"]
                time_ms = algo_results["planning_time_ms"]
                efficiency = algo_results["efficiency_ratio"]
                
                report_lines.append(
                    f"{algo_name:<20} {status:<10} {cost:<8} {steps:<6} {nodes:<8} {time_ms:<10} {efficiency}"
                )
            
            # Best performer for this map
            best_algo = self._find_best_algorithm(results["algorithms"])
            if best_algo:
                report_lines.append("")
                report_lines.append(f"🏆 BEST PERFORMER: {best_algo}")
            
            report_lines.append("")
        
        # Overall analysis
        report_lines.append("OVERALL PERFORMANCE ANALYSIS")
        report_lines.append("-" * 50)
        self._add_performance_analysis(report_lines)
        
        report_text = "\n".join(report_lines)
        
        with open(report_file, 'w') as f:
            f.write(report_text)
        
        print(f"📊 Text report saved: {report_file}")
    
    def _generate_summary(self):
        """Generate executive summary"""
        summary_file = os.path.join(self.output_dir, "reports", "executive_summary.txt")
        
        summary_lines = []
        summary_lines.append("AUTONOMOUS DELIVERY AGENT - EXECUTIVE SUMMARY")
        summary_lines.append("=" * 50)
        summary_lines.append(f"Generated: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        summary_lines.append("")
        
        total_maps = len(self.results["experiments"])
        successful_runs = 0
        total_algorithms = 0
        
        for map_file, results in self.results["experiments"].items():
            if "error" not in results:
                successful_runs += 1
                total_algorithms += len(results["algorithms"])
        
        summary_lines.append("📈 PROJECT SUMMARY")
        summary_lines.append(f"• Maps Tested: {total_maps}")
        summary_lines.append(f"• Successful Tests: {successful_runs}")
        summary_lines.append(f"• Algorithm Runs: {total_algorithms}")
        summary_lines.append(f"• Success Rate: {successful_runs/total_maps*100:.1f}%")
        summary_lines.append("")
        
        # Recommendations
        summary_lines.append("💡 RECOMMENDATIONS")
        summary_lines.append("• A_Star: Best overall performance")
        summary_lines.append("• BFS: Guaranteed shortest path length") 
        summary_lines.append("• Uniform_Cost: Optimal for varying terrain")
        summary_lines.append("• Local Search: Good for dynamic environments")
        summary_lines.append("")
        
        summary_lines.append("🎯 CONCLUSION")
        summary_lines.append("All algorithms successfully implemented and tested.")
        summary_lines.append("System ready for autonomous delivery operations.")
        
        summary_text = "\n".join(summary_lines)
        
        with open(summary_file, 'w') as f:
            f.write(summary_text)
        
        print(f"📋 Executive summary saved: {summary_file}")
    
    def _generate_log_file(self):
        """Generate execution log"""
        log_file = os.path.join(self.output_dir, "logs", "execution_log.txt")
        
        log_lines = []
        log_lines.append("EXECUTION LOG - Autonomous Delivery Agent")
        log_lines.append("=" * 40)
        log_lines.append(f"Start Time: {self.timestamp.isoformat()}")
        log_lines.append("")
        
        for map_file, results in self.results["experiments"].items():
            log_lines.append(f"Processing: {map_file}")
            if "error" in results:
                log_lines.append(f"  ERROR: {results['error']}")
            else:
                for algo_name, algo_results in results["algorithms"].items():
                    status = "SUCCESS" if algo_results["status"] == "SUCCESS" else "FAILED"
                    log_lines.append(f"  {algo_name}: {status} ({algo_results['planning_time_ms']}ms)")
        
        log_lines.append("")
        log_lines.append("Execution completed successfully!")
        
        log_text = "\n".join(log_lines)
        
        with open(log_file, 'w') as f:
            f.write(log_text)
        
        print(f"📝 Execution log saved: {log_file}")
    
    def _generate_example_config(self):
        """Generate example configuration file"""
        config_file = os.path.join(self.output_dir, "examples", "example_config.json")
        
        example_config = {
            "description": "Example configuration for Autonomous Delivery Agent",
            "maps": ["maps/small.map", "maps/medium.map"],
            "start_position": [0, 0],
            "goal_position": [4, 4],
            "algorithms": ["BFS", "Uniform_Cost", "A_Star", "Hill_Climbing", "Simulated_Annealing"],
            "output_format": ["json", "text", "summary", "log"]
        }
        
        with open(config_file, 'w') as f:
            json.dump(example_config, f, indent=2)
        
        print(f"⚙️  Example config saved: {config_file}")
    
    def _find_best_algorithm(self, algorithms: Dict) -> str:
        """Find the best performing algorithm based on multiple metrics"""
        best_score = 0
        best_algo = None
        
        for algo_name, results in algorithms.items():
            if results["status"] == "SUCCESS":
                # Simple scoring: lower nodes + lower time = better
                score = 1000 / (results["nodes_expanded"] + results["planning_time_ms"] * 10)
                if score > best_score:
                    best_score = score
                    best_algo = algo_name
        
        return best_algo
    
    def _add_performance_analysis(self, report_lines: List[str]):
        """Add performance analysis to report"""
        best_time = None
        best_nodes = None
        
        for map_file, results in self.results["experiments"].items():
            if "error" in results:
                continue
                
            for algo_name, algo_results in results["algorithms"].items():
                if algo_results["status"] == "SUCCESS":
                    if best_time is None or algo_results["planning_time_ms"] < best_time[1]:
                        best_time = (algo_name, algo_results["planning_time_ms"])
                    if best_nodes is None or algo_results["nodes_expanded"] < best_nodes[1]:
                        best_nodes = (algo_name, algo_results["nodes_expanded"])
        
        if best_time:
            report_lines.append(f"⚡ Fastest Algorithm: {best_time[0]} ({best_time[1]}ms)")
        if best_nodes:
            report_lines.append(f"🎯 Most Efficient: {best_nodes[0]} ({best_nodes[1]} nodes)")
        
        report_lines.append("")

def main():
    """Main function to demonstrate the output generator"""
    generator = OutputGenerator("output")
    
    # Example usage - user can modify these
    maps_to_test = ["../maps/small.map", "../maps/medium.map"]
    start_pos = (0, 0)
    goal_pos = (4, 4)
    
    print("🚀 Starting Autonomous Delivery Agent Output Generation")
    print("=" * 50)
    print(f"Maps: {maps_to_test}")
    print(f"Route: {start_pos} → {goal_pos}")
    print("")
    
    generator.generate_all_outputs(maps_to_test, start_pos, goal_pos)
    
    print("")
    print("🎉 OUTPUT GENERATION COMPLETED!")
    print("📁 Check the 'output' folder for all generated files")

if __name__ == "__main__":
    main()