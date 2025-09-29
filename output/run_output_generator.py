#!/usr/bin/env python3
"""
User-friendly output generator runner
Allows users to easily generate outputs with their own parameters
"""

import argparse
import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

from output_generator import OutputGenerator

def main():
    parser = argparse.ArgumentParser(
        description='Autonomous Delivery Agent - Output Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_output_generator.py --maps maps/small.map --start 0,0 --goal 4,4
  python run_output_generator.py --maps maps/small.map maps/medium.map --start 1,1 --goal 9,9
  python run_output_generator.py --config my_config.json
        """
    )
    
    parser.add_argument('--maps', nargs='+', help='Map files to test')
    parser.add_argument('--start', type=str, help='Start position (x,y)')
    parser.add_argument('--goal', type=str, help='Goal position (x,y)')
    parser.add_argument('--output-dir', default='output', help='Output directory')
    parser.add_argument('--config', help='Configuration file (JSON)')
    
    args = parser.parse_args()
    
    # Determine parameters
    if args.config:
        # Load from config file (you can implement this)
        print("📋 Loading configuration from file...")
        # Implement config file loading here
        maps = ["../maps/small.map"]
        start = (0, 0)
        goal = (4, 4)
    else:
        # Use command line arguments
        if not args.maps or not args.start or not args.goal:
            print("❌ Please provide maps, start, and goal parameters")
            print("💡 Use --help for usage information")
            return
        
        maps = args.maps
        start = tuple(map(int, args.start.split(',')))
        goal = tuple(map(int, args.goal.split(',')))
    
    print("🚀 Starting Output Generation")
    print("=" * 40)
    print(f"Output Directory: {args.output_dir}")
    print(f"Maps: {maps}")
    print(f"Start: {start}")
    print(f"Goal: {goal}")
    print("")
    
    # Generate outputs
    generator = OutputGenerator(args.output_dir)
    generator.generate_all_outputs(maps, start, goal)
    
    print("")
    print("✅ Output generation completed!")
    print(f"📁 Check {args.output_dir} folder for results")

if __name__ == "__main__":
    main()