
import os
import sys
import yaml
from unittest.mock import patch, MagicMock
# Add the directory to sys.path to import the module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import CollectFeedbackYaml

def test_collect_feedback():
    # Create a dummy file for testing
    test_file = "test_dummy.js" 
    with open(test_file, "w") as f:
        f.write("console.log('Hello');")
        
    try:
        # Mock input to return specific feedback
        with patch('builtins.input', return_value="Test feedback for dummy file"):
            # Mock os.walk to only return our test file
            # We need to replicate the yield structure: (root, dirs, files)
            def mock_walk(*args, **kwargs):
                yield ('.', [], [test_file])
            
            with patch('os.walk', side_effect=mock_walk):
                # Run the function (now calls collect_feedback_watcher)
                CollectFeedbackYaml.collect_feedback_yaml()
                
        # Check if YAML was created (new filename format)
        expected_output = "watcher_batch_1.yaml"
        if os.path.exists(expected_output):
            print(f"SUCCESS: {expected_output} created.")
            with open(expected_output, 'r') as f:
                data = yaml.safe_load(f)
                print("YAML Content:")
                print(yaml.dump(data, sort_keys=False))
                
                # Verify new structure
                assert 'metadata' in data, "Missing 'metadata' field"
                assert 'architecture_rules' in data, "Missing 'architecture_rules' field"
                assert 'watcher_validation_prompt' in data, "Missing 'watcher_validation_prompt' field"
                assert 'files' in data, "Missing 'files' field"
                
                # Verify file structure
                if data['files']:
                    file_entry = data['files'][0]
                    assert 'layer' in file_entry, "Missing 'layer' field in file entry"
                    assert 'role' in file_entry, "Missing 'role' field in file entry"
                    assert 'path' in file_entry, "Missing 'path' field in file entry"
                    assert 'source' in file_entry, "Missing 'source' field in file entry"
                    assert 'instruction' in file_entry, "Missing 'instruction' field in file entry"
                    
                print("\nAll structure validations passed!")
                
            # Clean up YAML
            os.remove(expected_output)
        else:
            print(f"FAILURE: {expected_output} not found.")

    finally:
        # Clean up test file
        if os.path.exists(test_file):
            os.remove(test_file)

if __name__ == "__main__":
    test_collect_feedback()
