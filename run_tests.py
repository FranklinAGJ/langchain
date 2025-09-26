#!/usr/bin/env python3
"""Simple test runner script."""
import subprocess
import sys

def run_tests():
    """Run the test suite."""
    try:
        result = subprocess.run(['python', '-m', 'pytest'], check=True)
        print("✅ All tests passed!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Some tests failed!")
        return False
    except FileNotFoundError:
        print("❌ pytest not found. Install with: pip install pytest")
        return False

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)