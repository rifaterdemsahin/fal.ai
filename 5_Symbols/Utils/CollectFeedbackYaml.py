import os
import yaml

def collect_feedback_yaml():
    # --- CONFIGURATION ---
    IGNORE_LIST = {'.git', '.venv', '__pycache__', '.DS_Store', 'feedback_output.txt', 'feedback_batches'}
    OUTPUT_FILE = "feedback_session.yaml"
    
    # Initialize output file if it doesn't exist
    if not os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            # We'll start with an empty list so we can append documents
            # However, standard YAML doesn't support appending to a list easily without reading the whole file.
            # A better approach for a stream of feedback is using multi-document YAML (separate documents)
            # or just appending to a list if we accept reading/writing.
            # Let's go with appending individual YAML documents for robustness and speed.
            pass

    # Load existing feedback to skip already processed files
    processed_files = set()
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                # yaml.safe_load_all returns a generator of all documents in the file
                for doc in yaml.safe_load_all(f):
                    if doc and 'file_path' in doc:
                        processed_files.add(doc['file_path'])
        except Exception as e:
            print(f"Warning: Could not read existing feedback file: {e}")

    files_to_process = []
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in IGNORE_LIST]
        for file in files:
            if file not in IGNORE_LIST and not file.endswith(('.yaml', '.pyc', '.png', '.jpg', '.jpeg', '.gif', '.svg')):
                full_path = os.path.join(root, file)
                if full_path not in processed_files:
                    files_to_process.append(full_path)

    if not files_to_process:
        print("No new files found to process (all have feedback).")
        return

    for i, file_path in enumerate(files_to_process):
        # Clear screen for better readability
        # os.name is 'posix' for macOS/Linux, 'nt' for Windows
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
        
        print(f"\n###########################################################")
        print(f"REVIEWING: {file_path}")
        print(f"###########################################################\n")
        print(f"[{i+1}/{len(files_to_process)}] - Reading content...\n")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            content = f"[Unreadable/Binary File: {e}]"

        print(f"\n--- BEGIN CONTENT: {file_path} ---")
        print(content)
        print(f"--- END CONTENT: {file_path} ---\n")

        try:
            feedback = input(f"Feedback for {os.path.basename(file_path)} (Enter to skip): ").strip()
        except EOFError:
            print("\nInput stream closed, stopping.")
            break
        
        if feedback:
            # Create a dictionary for the current entry
            file_entry = {
                'file_path': file_path,
                'instructions': feedback,
                'timestamp': os.popen('date -u +"%Y-%m-%dT%H:%M:%SZ"').read().strip()
            }
            
            # Append immediately to the file
            with open(OUTPUT_FILE, 'a', encoding='utf-8') as yfile:
                # Use explicit document separator to allow multiple entries
                yfile.write("---\n")
                yaml.dump(file_entry, yfile, sort_keys=False, default_flow_style=False)
            
            print(f">>> SAVED feedback for {os.path.basename(file_path)} to {OUTPUT_FILE} <<<")
            print("###############################\n")

if __name__ == "__main__":
    collect_feedback_yaml()
