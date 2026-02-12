import unittest
import sys
import os
from pathlib import Path
import datetime

class BaseAssetGeneratorTest(unittest.TestCase):
    """
    Base class for all asset generator tests.
    Provides common setup, teardown, and helper methods.
    """
    
    @classmethod
    def setUpClass(cls):
        """Set up paths and environment once for the test class"""
        cls.project_root = Path(__file__).resolve().parent.parent.parent
        cls.symbols_path = cls.project_root / "5_Symbols"
        if str(cls.symbols_path) not in sys.path:
            sys.path.append(str(cls.symbols_path))
        
        # Ensure TestOutput directory exists
        cls.test_output_root = cls.project_root / "7_TestingKnown" / "TestOutput" / "generated_assets"
        cls.test_output_root.mkdir(parents=True, exist_ok=True)
        
    def setUp(self):
        """Setup before each test"""
        self.start_time = datetime.datetime.now()

    def verify_environment(self):
        """Check if FAL_KEY is set"""
        if not os.environ.get("FAL_KEY"):
            self.skipTest("FAL_KEY environment variable not set")
            return False
        return True
    
    def assertFilesGenerated(self, directory: Path, extensions: list[str], min_count: int = 1):
        """Assert that files with given extensions were generated in the directory"""
        found_files = []
        for ext in extensions:
            found_files.extend(list(directory.glob(f"*{ext}")))
        
        self.assertTrue(len(found_files) >= min_count, 
                        f"Expected at least {min_count} files with extensions {extensions}, found {len(found_files)} in {directory}")
        return found_files

    @staticmethod
    def format_test_result(test_name, status, output_dir, generated_files):
        """Format the test result for the master report"""
        return {
            "test_name": test_name,
            "status": status,
            "timestamp": datetime.datetime.now().isoformat(),
            "output_dir": str(output_dir),
            "generated_files": [f.name for f in generated_files]
        }
