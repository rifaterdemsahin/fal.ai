#!/usr/bin/env python3
"""
Unit tests for 3D asset generator
"""

import unittest
import sys
import os
from pathlib import Path

# Add symbol root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "5_Symbols"))

from ThreeD.ThreeDGenerator import ThreeDAssetGenerator
from base.generator_config import OUTPUT_FORMATS, DEFAULT_MODELS


from base_test import BaseAssetGeneratorTest

class Test3DGenerator(BaseAssetGeneratorTest):
    """Test the ThreeDAssetGenerator class"""
    
    def test_generator_initialization(self):
        """Test that the generator initializes correctly"""
        generator = ThreeDAssetGenerator()
        
        # Check asset type
        self.assertEqual(generator.asset_type, "3d")
        
        # Check output format
        self.assertEqual(generator.output_format, "glb")
    
    def test_generation_queue_exists(self):
        """Test that generation queue is properly defined"""
        generator = ThreeDAssetGenerator()
        queue = generator.get_generation_queue()
        
        # Check that queue is not empty
        self.assertGreater(len(queue), 0)
        
        # Check that all items have required fields
        for item in queue:
            self.assertIn("id", item)
            self.assertIn("name", item)
            self.assertIn("prompt", item)
            self.assertIn("model", item)
            self.assertIn("priority", item)
    
    def test_model_configuration(self):
        """Test that the correct model is configured"""
        generator = ThreeDAssetGenerator()
        queue = generator.get_generation_queue()
        
        # Check that all items use the Hunyuan-3D model
        for item in queue:
            self.assertEqual(item["model"], "fal-ai/hunyuan-3d/v3.1/rapid/text-to-3d")
    
    def test_output_format_configuration(self):
        """Test that 3D output format is configured correctly"""
        # Check that 3D format is in OUTPUT_FORMATS
        self.assertIn("3d", OUTPUT_FORMATS)
        self.assertEqual(OUTPUT_FORMATS["3d"], "glb")
    
    def test_default_model_configuration(self):
        """Test that 3D default model is configured"""
        # Check that 3D model is in DEFAULT_MODELS
        self.assertIn("3d", DEFAULT_MODELS)
        self.assertEqual(DEFAULT_MODELS["3d"], "fal-ai/hunyuan-3d/v3.1/rapid/text-to-3d")
    
    def test_priority_levels(self):
        """Test that assets have valid priority levels"""
        generator = ThreeDAssetGenerator()
        queue = generator.get_generation_queue()
        
        valid_priorities = {"HIGH", "MEDIUM", "LOW"}
        for item in queue:
            self.assertIn(item["priority"], valid_priorities)
    
    def test_extract_result_url(self):
        """Test URL extraction from Hunyuan-3D response format"""
        generator = ThreeDAssetGenerator()
        
        # Test with Hunyuan-3D response format
        result = {
            "model_urls": {
                "glb": {
                    "url": "https://example.com/model.glb",
                    "content_type": "model/gltf-binary",
                    "file_name": "model.glb"
                },
                "obj": {
                    "url": "https://example.com/model.obj",
                    "content_type": "text/plain",
                    "file_name": "model.obj"
                }
            }
        }
        
        url = generator.extract_result_url(result, {})
        self.assertEqual(url, "https://example.com/model.glb")


class TestBatchAssetGenerator3D(BaseAssetGeneratorTest):
    """Test the batch 3D asset generator module"""
    
    def test_module_imports(self):
        """Test that the module can be imported"""
        try:
            from ThreeD import BatchAssetGenerator3D
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import BatchAssetGenerator3D: {e}")
    
    def test_seeds_configuration(self):
        """Test that SEEDS are configured in the batch generator"""
        # Imports in test are fine when dealing with potential import issues in dev
        from ThreeD import BatchAssetGenerator3D
        
        self.assertIn("SEED_001", BatchAssetGenerator3D.SEEDS)
        self.assertIn("SEED_002", BatchAssetGenerator3D.SEEDS)
    
    def test_generation_queue(self):
        """Test that GENERATION_QUEUE is properly configured"""
        from ThreeD import BatchAssetGenerator3D
        
        # Check that queue exists and is not empty
        self.assertGreater(len(BatchAssetGenerator3D.GENERATION_QUEUE), 0)
        
        # Check that all items have required fields
        for item in BatchAssetGenerator3D.GENERATION_QUEUE:
            self.assertIn("id", item)
            self.assertIn("name", item)
            self.assertIn("prompt", item)
            self.assertIn("model", item)


class TestIntegrationGeneration(BaseAssetGeneratorTest):
    """Integration tests that actually run generation"""
    
    def setUp(self):
        # We need to call the super setup as well if it had logic, but here we define new logic
        super().setUp()
        self.test_output_dir = self.test_output_root / "3d"
        self.test_output_dir.mkdir(parents=True, exist_ok=True)
        
    def test_run_generation(self):
        """Test actual generation of a 3D asset"""
        from ThreeD import BatchAssetGenerator3D
        
        # Create a single test item to avoid high costs
        test_queue = [
            {
                "id": "TEST_3D_001",
                "name": "test_cube",
                "priority": "HIGH",
                "scene": "Test Scene",
                "seed_key": "SEED_001",
                "prompt": "A simple white cube, 3d, minimalistic",
                "model": "fal-ai/hunyuan-3d/v3.1/rapid/text-to-3d"
            }
        ]
        
        print(f"\n🚀 Running integration test generation to {self.test_output_dir}...")
        
        # Run generation
        if not self.verify_environment():
            return
            
        results = BatchAssetGenerator3D.process_queue(test_queue, self.test_output_dir)
        
        # Verify success
        self.assertGreater(len(results["success"]), 0, "Should have generated at least one asset")
        self.assertEqual(len(results["failed"]), 0, "Should have zero failures")
        
        # Verify files exist using helper from BaseAssetGeneratorTest
        self.assertTrue(any(self.test_output_dir.glob("*.glb")) or any(self.test_output_dir.glob("*.obj")), "Should have created .glb or .obj files")
        
        glb_files = list(self.test_output_dir.glob("*.glb"))
        obj_files = list(self.test_output_dir.glob("*.obj"))
        json_files = list(self.test_output_dir.glob("*.json"))
        
        print(f"✅ Generated {len(glb_files)} GLB files, {len(obj_files)} OBJ files and {len(json_files)} JSON files")

def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add tests
    suite.addTests(loader.loadTestsFromTestCase(Test3DGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestBatchAssetGenerator3D))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegrationGeneration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    exit(run_tests())
