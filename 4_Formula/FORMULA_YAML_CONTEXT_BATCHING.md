# FORMULA_YAML_CONTEXT_BATCHING

> 📜 In 2026, **YAML** is often the preferred choice for AI context because it is significantly more **human-readable** than JSON and less "noisy" than XML. It uses indentation to define structure, which helps the AI understand the hierarchy of your repository without wasting tokens on closing tags.

## 🎯 Usecase in Weekly Artifact Generation

This formula outlines a method for efficiently communicating code context and change requests to AI assistants during weekly development sprints. By batching files and instructions into a clean YAML format, developers can ensure that the AI receives structured, token-efficient input, leading to more accurate code generation and refactoring suggestions. This is particularly useful when iterating on multiple files simultaneously or providing bulk feedback.

## 💡 The Best Practice: YAML-Formatted Context

Using YAML allows you to create a "manifest" of your changes. By structuring your output into a list of file objects, you provide a clean template that Copilot can follow line-by-line.

---

## 🛠️ The YAML Batch Collector Script

This script collects your feedback and saves it in a `.yaml` format. It uses **Batching** (5 files per batch) to ensure you don't overwhelm the AI's "reasoning" capabilities in a single turn.

The script is located at: `5_Symbols/Utils/CollectFeedbackYaml.py`

### Source Code

```python
import os
import yaml

def collect_feedback_yaml():
    # --- CONFIGURATION ---
    IGNORE_LIST = {'.git', '.venv', '__pycache__', '.DS_Store', 'feedback_output.txt'}
    BATCH_SIZE = 5 
    
    files_to_process = []
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in IGNORE_LIST]
        for file in files:
            if file not in IGNORE_LIST and not file.endswith(('.txt', '.yaml', '.py')):
                files_to_process.append(os.path.join(root, file))

    if not files_to_process:
        print("No files found to process.")
        return

    current_batch_data = []
    batch_count = 1

    for i, file_path in enumerate(files_to_process):
        print(f"\n[{i+1}/{len(files_to_process)}] FILE: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            content = "[Unreadable/Binary File]"

        feedback = input(f"Feedback for {os.path.basename(file_path)} (Enter to skip): ").strip()
        
        if feedback:
            # Create a dictionary for the YAML structure
            file_entry = {
                'file_path': file_path,
                'original_code': content,
                'instructions': feedback
            }
            current_batch_data.append(file_entry)

        # Save batch when size reached or at the very end
        if len(current_batch_data) == BATCH_SIZE or (i == len(files_to_process) - 1 and current_batch_data):
            output_name = f"repo_fix_batch_{batch_count}.yaml"
            
            payload = {
                'batch_info': {
                    'batch_number': batch_count,
                    'total_files_in_batch': len(current_batch_data)
                },
                'files': current_batch_data
            }

            with open(output_name, 'w', encoding='utf-8') as yfile:
                yaml.dump(payload, yfile, sort_keys=False, default_flow_style=False)
            
            print(f"\n>>> SAVED {output_name} <<<")
            current_batch_data = []
            batch_count += 1

if __name__ == "__main__":
    collect_feedback_yaml()
```

---

## 📝 Sample YAML Output Structure

Your `repo_fix_batch_1.yaml` will look like this, which is incredibly easy for an AI to parse:

```yaml
batch_info:
  batch_number: 1
  total_files_in_batch: 2
files:
  - file_path: ./src/utils.py
    original_code: |
      def add(a, b):
          return a + b
    instructions: Add type hinting and a docstring to this function.
  - file_path: ./src/main.py
    original_code: |
      print(add(5, 10))
    instructions: Import the add function correctly from utils.
```

---

## 🚀 Why YAML is superior for "Multiplication"

1. **Block Scalars (`|`):** The pipe symbol in YAML allows the code to be preserved exactly as it is (including newlines and indentation) without needing escape characters like `\n`.
2. **Clean Separation:** Each file starts with a `-`, making it a distinct item in a list.
3. **Low Token Overhead:** You aren't wasting tokens on `</file_path></original_code>` tags, meaning you can fit **more code** into a single prompt.

## 🤖 How to run this with Copilot

1. **Upload:** Provide `repo_fix_batch_1.yaml`.
2. **Command:** "I am providing a YAML manifest of my repository and the required changes. Please read the `instructions` for each `file_path` and provide the updated code."
