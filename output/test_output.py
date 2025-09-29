#!/usr/bin/env python3
"""
Quick test script for the output generator
"""

import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

from output_generator import OutputGenerator

def test_basic():
    """Test basic functionality"""
    print("🧪 Testing Output Generator...")
    
    generator = OutputGenerator("test_output")
    
    # Test with small map
    maps = ["../maps/small.map"]
    start = (0, 0)
    goal = (4, 4)
    
    print("Running basic test...")
    results = generator.generate_all_outputs(maps, start, goal)
    
    print("✅ Test completed successfully!")
    print(f"Generated outputs for {len(results['experiments'])} maps")

if __name__ == "__main__":
    test_basic()