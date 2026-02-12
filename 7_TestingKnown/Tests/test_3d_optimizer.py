#!/usr/bin/env python3
"""
Unit tests for Batch3DModelOptimizer
"""

import unittest
import tempfile
import os
from pathlib import Path
import sys

try:
    from base_test import BaseAssetGeneratorTest
except ImportError:
    sys.path.append(str(Path(__file__).resolve().parent))
    from base_test import BaseAssetGeneratorTest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "5_Symbols"))
from ThreeD.Batch3DModelOptimizer import (
    Model3DConfig,
    Model3DMetadata,
    Model3DValidator,
    Model3DOptimizer
)

class TestModel3DValidator(BaseAssetGeneratorTest):
    """Test the Model3DValidator class"""
    
    def setUp(self):
        super().setUp()
        self.validator = Model3DValidator()
        self.temp_dir = tempfile.mkdtemp() # Keep using tempfile for isolated tests or use self.test_output_root
        
    def tearDown(self):
        super().tearDown()
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_validator_initialization(self):
        """Test that validator initializes correctly"""
        self.assertEqual(len(self.validator.errors), 0)
        self.assertEqual(len(self.validator.warnings), 0)
    
    def test_validate_missing_file(self):
        """Test validation of non-existent file"""
        result = self.validator.validate("/nonexistent/file.glb")
        self.assertFalse(result)
        self.assertGreater(len(self.validator.errors), 0)
    
    def test_validate_unsupported_format(self):
        """Test validation of unsupported format"""
        test_file = Path(self.temp_dir) / "test.txt"
        test_file.write_text("dummy")
        
        result = self.validator.validate(str(test_file))
        self.assertFalse(result)
        self.assertIn("Unsupported format", self.validator.errors[0])
    
    def test_validate_glb_invalid(self):
        """Test validation of invalid GLB file"""
        test_file = Path(self.temp_dir) / "test.glb"
        test_file.write_bytes(b"invalid data")
        
        result = self.validator.validate_glb(str(test_file))
        self.assertFalse(result)
    
    def test_validate_glb_valid_header(self):
        """Test validation of GLB with valid header"""
        test_file = Path(self.temp_dir) / "test.glb"
        # Create minimal GLB header: magic + version + length
        header = b'glTF' + (2).to_bytes(4, 'little') + (100).to_bytes(4, 'little')
        test_file.write_bytes(header + b'\x00' * 88)  # Pad to 100 bytes
        
        result = self.validator.validate_glb(str(test_file))
        self.assertTrue(result)
    
    def test_validate_obj_valid(self):
        """Test validation of valid OBJ file"""
        test_file = Path(self.temp_dir) / "test.obj"
        obj_content = """# Test OBJ file
v 0.0 0.0 0.0
v 1.0 0.0 0.0
v 0.0 1.0 0.0
f 1 2 3
"""
        test_file.write_text(obj_content)
        
        result = self.validator.validate_obj(str(test_file))
        self.assertTrue(result)
    
    def test_validate_obj_no_vertices(self):
        """Test validation of OBJ file without vertices"""
        test_file = Path(self.temp_dir) / "test.obj"
        test_file.write_text("# Empty OBJ file\n")
        
        result = self.validator.validate_obj(str(test_file))
        self.assertFalse(result)
    
    def test_validate_dae_valid(self):
        """Test validation of valid DAE file"""
        test_file = Path(self.temp_dir) / "test.dae"
        dae_content = """<?xml version="1.0"?>
<COLLADA xmlns="http://www.collada.org/2005/11/COLLADASchema" version="1.4.1">
    <asset/>
</COLLADA>
"""
        test_file.write_text(dae_content)
        
        result = self.validator.validate_dae(str(test_file))
        self.assertTrue(result)


class TestModel3DConfig(BaseAssetGeneratorTest):
    """Test the Model3DConfig dataclass"""
    
    def test_config_defaults(self):
        """Test default configuration values"""
        config = Model3DConfig(
            input_path="input.glb",
            output_path="output.fbx"
        )
        
        self.assertEqual(config.target_format, "fbx")
        self.assertEqual(config.max_polygons, 1000000)
        self.assertTrue(config.embed_textures)
        self.assertTrue(config.optimize_geometry)
        self.assertEqual(config.target_scale, 1.0)
    
    def test_config_custom_values(self):
        """Test custom configuration values"""
        config = Model3DConfig(
            input_path="input.glb",
            output_path="output.obj",
            target_format="obj",
            max_polygons=500000,
            embed_textures=False
        )
        
        self.assertEqual(config.target_format, "obj")
        self.assertEqual(config.max_polygons, 500000)
        self.assertFalse(config.embed_textures)


class TestModel3DOptimizer(BaseAssetGeneratorTest):
    """Test the Model3DOptimizer class"""
    
    def setUp(self):
        super().setUp()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        super().tearDown()
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_optimizer_initialization(self):
        """Test optimizer initialization"""
        config = Model3DConfig(
            input_path="test.glb",
            output_path="output.fbx"
        )
        optimizer = Model3DOptimizer(config)
        
        self.assertIsNotNone(optimizer.config)
        self.assertIsNotNone(optimizer.validator)
    
    def test_analyze_glb_model(self):
        """Test analyzing a GLB model"""
        # Create a minimal valid GLB file
        test_file = Path(self.temp_dir) / "test.glb"
        header = b'glTF' + (2).to_bytes(4, 'little') + (100).to_bytes(4, 'little')
        test_file.write_bytes(header + b'\x00' * 88)
        
        config = Model3DConfig(
            input_path=str(test_file),
            output_path="output.fbx"
        )
        optimizer = Model3DOptimizer(config)
        
        metadata = optimizer.analyze_model(str(test_file))
        
        self.assertIsNotNone(metadata)
        self.assertEqual(metadata['source_format'], 'glb')
        self.assertEqual(metadata['filename'], 'test.glb')
        self.assertTrue(metadata['validated'])
    
    def test_analyze_obj_model(self):
        """Test analyzing an OBJ model"""
        test_file = Path(self.temp_dir) / "test.obj"
        obj_content = """v 0.0 0.0 0.0
v 1.0 0.0 0.0
v 0.0 1.0 0.0
f 1 2 3
"""
        test_file.write_text(obj_content)
        
        config = Model3DConfig(
            input_path=str(test_file),
            output_path="output.fbx"
        )
        optimizer = Model3DOptimizer(config)
        
        metadata = optimizer.analyze_model(str(test_file))
        
        self.assertIsNotNone(metadata)
        self.assertEqual(metadata['source_format'], 'obj')
        self.assertEqual(metadata['vertex_count'], 3)
        self.assertEqual(metadata['face_count'], 1)

if __name__ == "__main__":
    unittest.main()
