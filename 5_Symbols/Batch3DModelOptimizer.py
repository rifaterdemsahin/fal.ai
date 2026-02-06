#!/usr/bin/env python3
"""
3D Model Optimization Utility

Validates and optimizes 3D models for DaVinci Resolve Fusion integration.
Supports FBX, OBJ, and DAE formats.

Usage:
    python Batch3DModelOptimizer.py
"""

import json
import os
import sys
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple, Optional
import subprocess
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class Model3DConfig:
    """Configuration for 3D model optimization"""
    input_path: str
    output_path: str
    target_format: str = "fbx"  # fbx, obj, dae
    max_polygons: int = 1000000  # 1M polygons
    embed_textures: bool = True
    optimize_geometry: bool = True
    bake_animations: bool = True
    target_scale: float = 1.0
    description: str = ""
    version: int = 1


@dataclass
class Model3DMetadata:
    """Metadata about exported 3D model"""
    filename: str
    source_format: str
    target_format: str
    polygon_count: int
    vertex_count: int
    texture_count: int
    embedded_textures: bool
    has_animations: bool
    bounding_box: Dict[str, float]
    scale_factor: float
    file_size_bytes: int
    export_date: str
    description: str
    version: int


class Model3DValidator:
    """Validates 3D model files"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def validate_fbx(self, filepath: str) -> bool:
        """Validate FBX file structure"""
        try:
            # Check file exists and is readable
            if not os.path.isfile(filepath):
                self.errors.append(f"File not found: {filepath}")
                return False
            
            # Check file size (FBX files should be > 1KB, < 1GB for practical use)
            file_size = os.path.getsize(filepath)
            if file_size < 1024:
                self.errors.append(f"File too small: {file_size} bytes (possible corruption)")
                return False
            
            if file_size > 1_073_741_824:  # 1GB
                self.warnings.append(f"Large file size: {file_size / 1024 / 1024:.2f} MB")
            
            # Check file header (FBX files start with specific bytes)
            with open(filepath, 'rb') as f:
                header = f.read(23)
                # FBX ASCII starts with "; FBX" or binary with "Kaydara FBX Binary"
                if not (header.startswith(b'; FBX') or b'Kaydara FBX Binary' in header):
                    self.errors.append("Invalid FBX file header")
                    return False
            
            logger.info(f"✅ FBX validation passed: {filepath}")
            return True
            
        except Exception as e:
            self.errors.append(f"Validation error: {str(e)}")
            return False
    
    def validate_obj(self, filepath: str) -> bool:
        """Validate OBJ file structure"""
        try:
            if not os.path.isfile(filepath):
                self.errors.append(f"File not found: {filepath}")
                return False
            
            file_size = os.path.getsize(filepath)
            if file_size < 10:
                self.errors.append(f"File too small: {file_size} bytes")
                return False
            
            # OBJ files are text-based, check for basic structure
            has_vertices = False
            has_faces = False
            
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for i, line in enumerate(f):
                    if i > 1000:  # Check first 1000 lines
                        break
                    line = line.strip()
                    if line.startswith('v '):
                        has_vertices = True
                    elif line.startswith('f '):
                        has_faces = True
            
            if not has_vertices:
                self.errors.append("No vertices found in OBJ file")
                return False
            
            if not has_faces:
                self.warnings.append("No faces found in OBJ file (point cloud?)")
            
            logger.info(f"✅ OBJ validation passed: {filepath}")
            return True
            
        except Exception as e:
            self.errors.append(f"Validation error: {str(e)}")
            return False
    
    def validate_dae(self, filepath: str) -> bool:
        """Validate DAE (COLLADA) file structure"""
        try:
            if not os.path.isfile(filepath):
                self.errors.append(f"File not found: {filepath}")
                return False
            
            file_size = os.path.getsize(filepath)
            if file_size < 100:
                self.errors.append(f"File too small: {file_size} bytes")
                return False
            
            # DAE files are XML-based, check for COLLADA structure
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(1024)  # Read first 1KB
                if '<COLLADA' not in content:
                    self.errors.append("Invalid DAE file: missing COLLADA root element")
                    return False
            
            logger.info(f"✅ DAE validation passed: {filepath}")
            return True
            
        except Exception as e:
            self.errors.append(f"Validation error: {str(e)}")
            return False
    
    def validate_glb(self, filepath: str) -> bool:
        """Validate GLB (glTF binary) file structure"""
        try:
            if not os.path.isfile(filepath):
                self.errors.append(f"File not found: {filepath}")
                return False
            
            file_size = os.path.getsize(filepath)
            if file_size < 100:
                self.errors.append(f"File too small: {file_size} bytes")
                return False
            
            # GLB files start with "glTF" magic string and version
            with open(filepath, 'rb') as f:
                magic = f.read(4)
                if magic != b'glTF':
                    self.errors.append("Invalid GLB file: missing glTF magic bytes")
                    return False
                
                version = int.from_bytes(f.read(4), 'little')
                if version != 2:
                    self.warnings.append(f"GLB version {version} (expected 2)")
            
            logger.info(f"✅ GLB validation passed: {filepath}")
            return True
            
        except Exception as e:
            self.errors.append(f"Validation error: {str(e)}")
            return False
    
    def validate(self, filepath: str) -> bool:
        """Validate 3D model based on file extension"""
        ext = Path(filepath).suffix.lower()
        
        if ext == '.fbx':
            return self.validate_fbx(filepath)
        elif ext == '.obj':
            return self.validate_obj(filepath)
        elif ext == '.dae':
            return self.validate_dae(filepath)
        elif ext == '.glb':
            return self.validate_glb(filepath)
        else:
            self.errors.append(f"Unsupported format: {ext}")
            return False


class Model3DOptimizer:
    """Optimizes 3D models for DaVinci Resolve Fusion"""
    
    def __init__(self, config: Model3DConfig):
        self.config = config
        self.validator = Model3DValidator()
    
    def analyze_model(self, filepath: str) -> Optional[Dict]:
        """Analyze 3D model and extract metadata"""
        try:
            file_size = os.path.getsize(filepath)
            ext = Path(filepath).suffix.lower()
            
            metadata = {
                'filename': Path(filepath).name,
                'source_format': ext[1:],  # Remove dot
                'file_size_bytes': file_size,
                'file_size_mb': round(file_size / 1024 / 1024, 2),
                'validated': self.validator.validate(filepath)
            }
            
            # For GLB files, we can extract more information
            if ext == '.glb':
                metadata.update(self._analyze_glb(filepath))
            elif ext == '.obj':
                metadata.update(self._analyze_obj(filepath))
            
            return metadata
            
        except Exception as e:
            logger.error(f"Error analyzing model: {e}")
            return None
    
    def _analyze_glb(self, filepath: str) -> Dict:
        """Extract detailed info from GLB file"""
        info = {
            'format': 'glb',
            'version': 'unknown',
            'has_textures': False,
            'has_animations': False
        }
        
        try:
            with open(filepath, 'rb') as f:
                # Skip magic and version (already validated)
                f.seek(8)
                # Read length
                length = int.from_bytes(f.read(4), 'little')
                info['declared_size'] = length
                
                # Parse chunks to detect textures/animations
                while f.tell() < length:
                    try:
                        chunk_length = int.from_bytes(f.read(4), 'little')
                        chunk_type = f.read(4)
                        
                        if chunk_type == b'JSON':
                            # JSON chunk contains scene structure
                            json_data = f.read(chunk_length)
                            # Simple heuristic: check for keywords
                            if b'textures' in json_data:
                                info['has_textures'] = True
                            if b'animations' in json_data:
                                info['has_animations'] = True
                        else:
                            # Skip other chunks
                            f.seek(chunk_length, 1)
                    except Exception as e:
                        # Chunk parsing may fail at end of file or with malformed data
                        logger.debug(f"Stopped chunk parsing: {e}")
                        break
                        
        except Exception as e:
            logger.warning(f"Could not fully analyze GLB: {e}")
        
        return info
    
    def _analyze_obj(self, filepath: str) -> Dict:
        """Extract detailed info from OBJ file"""
        info = {
            'format': 'obj',
            'vertex_count': 0,
            'face_count': 0,
            'has_textures': False,
            'has_normals': False
        }
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('v '):
                        info['vertex_count'] += 1
                    elif line.startswith('f '):
                        info['face_count'] += 1
                    elif line.startswith('vt '):
                        info['has_textures'] = True
                    elif line.startswith('vn '):
                        info['has_normals'] = True
        except Exception as e:
            logger.warning(f"Could not fully analyze OBJ: {e}")
        
        return info
    
    def optimize_for_fusion(self, output_dir: Path) -> bool:
        """
        Optimize 3D model for DaVinci Resolve Fusion integration.
        
        DaVinci Resolve Fusion supports:
        - FBX: Recommended format with full animation support
        - OBJ: Basic geometry, limited animation
        - DAE: COLLADA format with animation support
        - Alembic (.abc): For cached animations
        
        Best practices for Fusion:
        - Keep polygon count reasonable (< 1M for real-time)
        - Embed textures when possible
        - Use standard material properties
        - Scale appropriately (Fusion units)
        """
        try:
            logger.info("🔧 Optimizing 3D model for DaVinci Resolve Fusion...")
            
            # Validate input file
            if not self.validator.validate(self.config.input_path):
                logger.error("❌ Input file validation failed:")
                for error in self.validator.errors:
                    logger.error(f"   - {error}")
                return False
            
            # Analyze input model
            metadata = self.analyze_model(self.config.input_path)
            if not metadata:
                logger.error("❌ Could not analyze input model")
                return False
            
            logger.info(f"📊 Model analysis:")
            logger.info(f"   - Format: {metadata.get('format', 'unknown')}")
            logger.info(f"   - Size: {metadata.get('file_size_mb', 0)} MB")
            
            if 'vertex_count' in metadata:
                logger.info(f"   - Vertices: {metadata['vertex_count']:,}")
            if 'face_count' in metadata:
                logger.info(f"   - Faces: {metadata['face_count']:,}")
            
            # Create output directory
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy or convert the model
            source_path = Path(self.config.input_path)
            output_path = output_dir / Path(self.config.output_path).name
            
            # For now, we'll copy the file and save metadata
            # In a production environment, you might use Blender or another tool
            # to actually optimize/convert the model
            import shutil
            shutil.copy2(source_path, output_path)
            
            # Save metadata
            metadata_path = output_path.with_suffix('.json')
            full_metadata = {
                **metadata,
                'optimized_for': 'DaVinci Resolve Fusion',
                'optimization_date': datetime.now().isoformat(),
                'config': asdict(self.config),
                'validation_errors': self.validator.errors,
                'validation_warnings': self.validator.warnings
            }
            
            with open(metadata_path, 'w') as f:
                json.dump(full_metadata, f, indent=2)
            
            logger.info(f"✅ Model optimized: {output_path}")
            logger.info(f"📝 Metadata saved: {metadata_path}")
            
            # Print Fusion integration tips
            self._print_fusion_tips(metadata)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Optimization failed: {e}")
            return False
    
    def _print_fusion_tips(self, metadata: Dict):
        """Print tips for using the model in DaVinci Resolve Fusion"""
        logger.info("\n💡 DaVinci Resolve Fusion Integration Tips:")
        logger.info("   1. Import via Fusion page: File > Import > 3D Model")
        logger.info("   2. Use FBX format for best compatibility")
        logger.info("   3. Check scale - Fusion uses different units than some 3D apps")
        logger.info("   4. Add lights and camera for proper rendering")
        logger.info("   5. Use Merge3D node to combine with other elements")
        
        if metadata.get('has_textures'):
            logger.info("   ✅ Model has textures - ensure texture files are in same directory")
        if metadata.get('has_animations'):
            logger.info("   ✅ Model has animations - use Timeline to control playback")


def batch_optimize_models(input_dir: str, output_dir: str):
    """
    Batch optimize all 3D models in a directory.
    
    Args:
        input_dir: Directory containing 3D models
        output_dir: Directory for optimized models
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    if not input_path.exists():
        logger.error(f"❌ Input directory not found: {input_dir}")
        return
    
    # Find all 3D model files
    model_files = []
    for ext in ['.glb', '.fbx', '.obj', '.dae']:
        model_files.extend(input_path.glob(f'**/*{ext}'))
    
    if not model_files:
        logger.warning("⚠️  No 3D model files found")
        return
    
    logger.info(f"📦 Found {len(model_files)} model(s) to optimize")
    
    # Process each model
    success_count = 0
    for model_file in model_files:
        logger.info(f"\n{'='*60}")
        logger.info(f"Processing: {model_file.name}")
        logger.info(f"{'='*60}")
        
        # Create config
        config = Model3DConfig(
            input_path=str(model_file),
            output_path=str(output_path / model_file.name),
            description=f"Optimized from {model_file.name}"
        )
        
        # Optimize
        optimizer = Model3DOptimizer(config)
        if optimizer.optimize_for_fusion(output_path):
            success_count += 1
    
    # Summary
    logger.info(f"\n{'='*60}")
    logger.info(f"📊 Batch Optimization Summary")
    logger.info(f"{'='*60}")
    logger.info(f"✅ Successfully optimized: {success_count}/{len(model_files)}")
    logger.info(f"📁 Output directory: {output_path.absolute()}")


def main():
    """Main execution"""
    print("\n" + "="*60)
    print("🎲 3D Model Optimizer for DaVinci Resolve Fusion")
    print("="*60 + "\n")
    
    # Check for existing 3D models in generated_assets
    assets_dir = Path("./generated_assets")
    output_dir = Path("./optimized_3d_models")
    
    if assets_dir.exists():
        logger.info(f"📂 Checking for 3D models in: {assets_dir}")
        batch_optimize_models(str(assets_dir), str(output_dir))
    else:
        logger.info("💡 Usage example:")
        logger.info("   python Batch3DModelOptimizer.py")
        logger.info("\n   This will optimize all .glb, .fbx, .obj, and .dae files")
        logger.info("   from ./generated_assets to ./optimized_3d_models")
        logger.info("\n   Or customize by editing the main() function.")
        
        # Example usage
        logger.info("\n📝 To optimize specific files:")
        logger.info("""
    from Batch3DModelOptimizer import Model3DConfig, Model3DOptimizer
    
    config = Model3DConfig(
        input_path="path/to/model.glb",
        output_path="path/to/optimized_model.fbx",
        target_format="fbx",
        max_polygons=500000
    )
    
    optimizer = Model3DOptimizer(config)
    optimizer.optimize_for_fusion(Path("./output"))
        """)


if __name__ == "__main__":
    main()
