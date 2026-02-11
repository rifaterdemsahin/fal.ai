import os
import yaml
import re
from datetime import datetime

def collect_feedback_watcher():
    # --- DOMAIN DEFINITIONS ---
    DOMAIN_MAP = {
        'realunknown': 'OBJECTIVES & OKRs (The Why)',
        'environment': 'CONTEXT & CONFIG (The Where)',
        'simulation': 'SCENARIOS (The What-if)',
        'formula': 'LOGIC ENGINE (The How)',
        'symbols': 'LANDING ZONE (The Execution)',
        'semblance': 'ERROR MEMORY (The Safety Net)',
        'testingknown': 'VALIDATION (The Proof)'
    }
    
    FOLDER_ORDER = list(DOMAIN_MAP.keys())
    IGNORE_LIST = {'.git', '.venv', '__pycache__', 'node_modules'}
    BATCH_SIZE = 5

    def get_priority(path):
        # Extract and normalize path components for accurate matching
        # Remove underscores and leading digits from each component
        path_components = [re.sub(r'^\d+', '', p.lower().replace('_', '')) 
                          for p in os.path.normpath(path).split(os.sep)]
        for i, folder in enumerate(FOLDER_ORDER):
            # Check if the folder key matches a complete path component (not substring)
            if folder in path_components:
                return i
        return 999

    # 1. Gather and Prioritize
    all_files = []
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in IGNORE_LIST]
        for file in files:
            # Exclude existing batches and script files
            if not file.endswith(('.yaml', '.pyc', '.txt')) and file != os.path.basename(__file__):
                all_files.append(os.path.join(root, file))

    all_files.sort(key=get_priority)

    current_batch = []
    batch_num = 1

    # 2. Interactive Feedback Loop
    print(f"--- WATCHER MODE START ({len(all_files)} files) ---")
    for i, file_path in enumerate(all_files):
        # Extract and normalize path components for accurate matching
        # Remove underscores and leading digits from each component
        path_components = [re.sub(r'^\d+', '', p.lower().replace('_', '')) 
                          for p in os.path.normpath(file_path).split(os.sep)]
        folder_key = next((f for f in FOLDER_ORDER if f in path_components), 'unknown')
        role = DOMAIN_MAP.get(folder_key, 'General Context')

        print(f"\n[{folder_key.upper()}] {file_path}")
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
        except:
            content = "[File unreadable]"

        feedback = input("Define Change/Requirement: ").strip()
        
        if feedback:
            current_batch.append({
                'layer': folder_key,
                'role': role,
                'path': file_path,
                'source': content,
                'instruction': feedback
            })

        # 3. Save with Watcher Validation Logic
        if len(current_batch) == BATCH_SIZE or (i == len(all_files) - 1 and current_batch):
            output_name = f"watcher_batch_{batch_num}.yaml"
            
            data = {
                'metadata': {
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M"),
                    'batch': batch_num,
                    'hierarchy_rules': "Changes in SYMBOLS must be justified by objectives in REAL."
                },
                'architecture_rules': DOMAIN_MAP,
                'watcher_validation_prompt': (
                    "Before writing any code, explain how these changes "
                    "align with the 'real' objectives and how they will be "
                    "verified in 'testing'."
                ),
                'files': current_batch
            }

            with open(output_name, 'w', encoding='utf-8') as y:
                yaml.dump(data, y, sort_keys=False, default_flow_style=False)
            
            print(f"\n[SYSTEM] {output_name} generated with Watcher Validation tags.")
            current_batch = []
            batch_num += 1

def collect_feedback_yaml():
    """Legacy function name kept for backwards compatibility"""
    collect_feedback_watcher()

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
    collect_feedback_watcher()
