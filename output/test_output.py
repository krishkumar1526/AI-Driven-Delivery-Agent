#!/usr/bin/env python3
"""
Quick test script for the output generator
"""

import os
import sys
import json
import numpy as np

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Custom JSON encoder to handle numpy types
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.bool_):
            return bool(obj)
        return super().default(obj)

from output_generator import OutputGenerator

def test_basic():
    """Test basic functionality"""
    print("🧪 Testing Output Generator...")
    
    generator = OutputGenerator("test_output")
    
    # Test with small map - adjust path since we're in 'output' folder
    maps = ["./maps/small.map"]  # or "../maps/small.map"
    start = (0, 0)
    goal = (4, 4)
    
    print("Running basic test...")
    
    try:
        results = generator.generate_all_outputs(maps, start, goal)
        
        # Use custom encoder for any JSON operations
        json_output = json.dumps(results, cls=NumpyEncoder, indent=2)
        print("✅ Test completed successfully!")
        print(f"Generated outputs for {len(results['experiments'])} maps")
        
    except TypeError as e:
        if "JSON serializable" in str(e):
            print("❌ JSON Serialization Error - Need to fix output_generator.py")
            print("The main generator file needs to use NumpyEncoder")
            print("Let's also fix the output_generator.py file...")
        else:
            raise e
    except Exception as e:
        print(f"❌ Other error: {e}")

if __name__ == "__main__":
    test_basic()