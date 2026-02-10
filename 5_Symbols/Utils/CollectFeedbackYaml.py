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
            if file not in IGNORE_LIST and not file.endswith(('.yaml', '.pyc', '.png', '.jpg', '.jpeg', '.gif', '.svg')):
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
