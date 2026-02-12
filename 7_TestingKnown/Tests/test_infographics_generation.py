#!/usr/bin/env python3
"""
Test script for Infographics Generator with fal.ai integration.

This script validates the BatchAssetGeneratorInfographics module by running
a small test batch and verifying the output.
"""
import sys
import unittest
from pathlib import Path
from typing import Dict, List, Any
import datetime

try:
    from base_test import BaseAssetGeneratorTest
except ImportError:
    sys.path.append(str(Path(__file__).resolve().parent))
    from base_test import BaseAssetGeneratorTest

class TestInfographicsGeneration(BaseAssetGeneratorTest):
    
    def setUp(self):
        super().setUp()
        self.output_dir = self.test_output_root / "infographics"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def import_generator(self):
        try:
            from Images import BatchAssetGeneratorInfographics
            return BatchAssetGeneratorInfographics
        except ImportError as e:
            self.fail(f"Failed to load BatchAssetGeneratorInfographics: {e}\nVerify module exists in 5_Symbols/Images/")

    def create_test_batch(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": "K8S_PODS_VAR1",
                "name": "kubernetes_pods_var1",
                "priority": "HIGH",
                "scene": "Kubernetes Architecture",
                "seed_key": "SEED_K8S_01",
                "prompt": "Infographic explaining Kubernetes Pods: The smallest deployable units of computing that you can create and manage in Kubernetes. Visualizing a pod wrapping a container. Include nano banana 3 in the design.",
                "image_size": {"width": 1920, "height": 1080},
                "model": "fal-ai/flux-pro/v1.1"
            },
            {
                "id": "K8S_PODS_VAR2",
                "name": "kubernetes_pods_var2",
                "priority": "HIGH",
                "scene": "Kubernetes Architecture",
                "seed_key": "SEED_K8S_02",
                "prompt": "Infographic explaining Kubernetes Pods: The smallest deployable units of computing that you can create and manage in Kubernetes. Visualizing a pod wrapping a container. Include nano banana 3 in the design.",
                "image_size": {"width": 1920, "height": 1080},
                "model": "fal-ai/flux-pro/v1.1"
            },
            {
                "id": "K8S_PODS_VAR3",
                "name": "kubernetes_pods_var3",
                "priority": "HIGH",
                "scene": "Kubernetes Architecture",
                "seed_key": "SEED_K8S_03",
                "prompt": "Infographic explaining Kubernetes Pods: The smallest deployable units of computing that you can create and manage in Kubernetes. Visualizing a pod wrapping a container. Include nano banana 3 in the design.",
                "image_size": {"width": 1920, "height": 1080},
                "model": "fal-ai/nano-banana-pro"
            }
        ]

    def test_infographics_generation(self):
        print(f"\n🚀 Infographics Generator Test Suite")
        
        if not self.verify_environment():
            return
        
        generator = self.import_generator()
        test_batch = self.create_test_batch()
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        for item in test_batch:
            item["name"] = f"{item['name']}_{timestamp}"

        print(f"🧪 Test Batch: {len(test_batch)} infographic(s)")
        print(f"📂 Output: {self.output_dir}")
        
        try:
            print("⏳ Generating assets...")
            generator.process_queue(test_batch, self.output_dir)
            
            generated = self.assertFilesGenerated(self.output_dir, [".png", ".jpg", ".jpeg"], min_count=1)
            
            print("\n" + "=" * 70)
            print("✅ TEST COMPLETE")
            print("=" * 70)
            print(f"\n📄 Generated Files:")
            for f in generated:
                size_kb = f.stat().st_size / 1024
                print(f"   • {f.name:<40} ({size_kb:>8.1f} KB)")
                
        except Exception as e:
            self.fail(f"Generation Failed: {e}")

if __name__ == "__main__":
    unittest.main()