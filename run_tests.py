"""
Standalone Test Runner for Datheon Python Programming Internship.
Executes all unit tests with zero third-party dependencies using Python's standard unittest library.
"""

import sys
import unittest
from pathlib import Path

# Add root and task directories to path
root_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(root_dir))
sys.path.insert(0, str(root_dir / "task1_hangman"))
sys.path.insert(0, str(root_dir / "task2_stock_portfolio"))
sys.path.insert(0, str(root_dir / "task3_file_organizer"))
sys.path.insert(0, str(root_dir / "task4_terminal_assistant"))
sys.path.insert(0, str(root_dir / "task5_enterprise_inventory"))


def run_all_tests():
    print("=" * 70)
    print("      🧪 DATHEON PYTHON INTERNSHIP: COMPREHENSIVE TEST SUITE 🧪      ")
    print("=" * 70)

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Discover and add all tests from tests directory
    discovered = loader.discover(start_dir=str(root_dir / "tests"), pattern="test_*.py")
    suite.addTests(discovered)

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 70)
    print(f"Tests Run: {result.testsRun} | Failures: {len(result.failures)} | Errors: {len(result.errors)}")
    if result.wasSuccessful():
        print("🎉 STATUS: 100% OF TESTS PASSED SUCCESSFULLY!")
        print("=" * 70)
        return 0
    else:
        print("❌ STATUS: TESTS FAILED!")
        print("=" * 70)
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
