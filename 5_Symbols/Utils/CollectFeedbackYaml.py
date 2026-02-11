import os
import yaml
import re
from datetime import datetime

# --- CONFIGURATION & CONSTANTS ---
BATCH_SIZE = 5
IGNORE_LIST = {'.git', '.venv', '__pycache__', '.DS_Store', 'feedback_output.txt', 'feedback_batches'}
OUTPUT_DIR = "7_TestingKnown/feedback_batches"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
WATCHER_FILENAME_PREFIX = "watcher_batch_"

# Maps normalized folder names to architectural roles
DOMAIN_MAP = {
    'real': 'OBJECTIVES & OKRs (The Why)',
    'realunknown': 'OBJECTIVES & OKRs (The Why)',
    'environment': 'CONTEXT & CONFIG (The Where)',
    'simulation': 'LOGIC ENGINE (The How)',
    'formula': 'LOGIC ENGINE (The How)',
    'symbols': 'LANDING ZONE (The Execution)',
    'semblance': 'VALIDATION & OUTPUT (The What)',
    'testing': 'VERIFICATION (The Proof)',
    'testingknown': 'VERIFICATION (The Proof)',
    'utils': 'UTILITIES & TOOLS',
    'root': 'PROJECT ROOT'
}

HIERARCHY_ORDER = [
    'realunknown', 'real',
    'environment',
    'simulation', 'formula',
    'symbols',
    'semblance',
    'testingknown', 'testing',
    'utils', 'root'
]

def normalize_key(name):
    """
    Normalizes directory names by removing leading digits/underscores and converting to lowercase.
    Example: '1_RealUnknown' -> 'realunknown'
    """
    normalized = re.sub(r'^[\d_]+', '', name).lower()
    return normalized

def get_role_and_layer(file_path):
    """
    Determines the layer and role based on the file path.
    Returns (layer_name, role_description).
    """
    parts = file_path.split(os.sep)
    found_layer = 'root'
    
    for part in parts:
        if part in ['.', '..']:
            continue
        norm = normalize_key(part)
        if norm in DOMAIN_MAP:
            found_layer = norm
            break
            
    role = DOMAIN_MAP.get(found_layer, "UNKNOWN LAYER")
    return found_layer, role

def get_hierarchy_index(layer):
    """Returns a sort index for the layer."""
    if layer in HIERARCHY_ORDER:
        return HIERARCHY_ORDER.index(layer)
    return len(HIERARCHY_ORDER)

def get_next_batch_number():
    """Finds the next batch number by scanning existing watcher_batch_N.yaml files."""
    max_num = 0
    pattern = re.compile(rf"{WATCHER_FILENAME_PREFIX}(\d+)\.yaml")
    for filename in os.listdir(OUTPUT_DIR):
        match = pattern.match(filename)
        if match:
            num = int(match.group(1))
            if num > max_num:
                max_num = num
    return max_num + 1

def collect_feedback_watcher():
    print("Starting Watcher Feedback Collector...")
    
    create_sample = input("Create a sample copy only? (y/N): ").strip().lower() == 'y'
    
    # 1. Identify processed files
    processed_files = set()
    pattern = re.compile(rf"{WATCHER_FILENAME_PREFIX}(\d+)\.yaml")
    
    # Check existing batches
    for filename in os.listdir(OUTPUT_DIR):
        if pattern.match(filename) or filename == 'feedback_session.yaml':
            try:
                with open(os.path.join(OUTPUT_DIR, filename), 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Try safe_load (new format)
                    try:
                        data = yaml.safe_load(content)
                        if isinstance(data, dict) and 'files' in data:
                            for entry in data['files']:
                                if 'path' in entry:
                                    processed_files.add(entry['path'])
                    except:
                        pass
                    # Try safe_load_all (legacy format)
                    try:
                        for doc in yaml.safe_load_all(content):
                            if doc and isinstance(doc, dict) and 'file_path' in doc:
                                processed_files.add(doc['file_path'])
                    except:
                        pass
            except Exception as e:
                print(f"Warning: Could not read {filename}: {e}")

    # 2. Collect files
    files_to_process = []
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in IGNORE_LIST]
        for file in files:
            if file not in IGNORE_LIST and not file.endswith(('.yaml', '.pyc', '.png', '.jpg', '.jpeg', '.gif', '.svg')):
                full_path = os.path.join(root, file)
                clean_path = os.path.relpath(full_path, '.')
                if clean_path.startswith('./'):
                    clean_path = clean_path[2:]
                
                if clean_path not in processed_files and ("./"+clean_path) not in processed_files:
                     files_to_process.append(clean_path)

    # 3. Sort by Hierarchy
    def sort_key(filepath):
        layer, _ = get_role_and_layer(filepath)
        return get_hierarchy_index(layer)

    files_to_process.sort(key=sort_key)

    if not files_to_process:
        print("No new files found to process.")
        return
    
    print(f"Found {len(files_to_process)} files to review.")
    
    # 4. Review Process
    current_batch_files = []
    
    for i, file_path in enumerate(files_to_process):
        # UI Cleanup
        if os.name == 'nt': os.system('cls')
        else: os.system('clear')

        layer, role = get_role_and_layer(file_path)
        
        print(f"\n###########################################################")
        print(f"WATCHER: REVIEWING [{layer.upper()}]")
        print(f"ROLE: {role}")
        print(f"FILE: {file_path}")
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

        print(f"Hierarchy Rule: Changes in {layer.upper()} must align with {role}.")
        
        try:
            if create_sample:
                feedback = f"Sample feedback for {os.path.basename(file_path)}"
                print(f"Sample Mode: Using '{feedback}'")
            else:
                feedback = input(f"Feedback/Justification for {os.path.basename(file_path)} (Enter to skip): ").strip()
        except EOFError:
            break

        if feedback:
            file_entry = {
                'layer': layer,
                'role': role,
                'path': "./" + file_path if not file_path.startswith("./") else file_path,
                'instruction': feedback
            }
            current_batch_files.append(file_entry)
            print(f">>> Added to batch. Current batch size: {len(current_batch_files)}")

        # Check for batch completion
        # Check for batch completion
        effective_batch_size = 1 if create_sample else BATCH_SIZE
        if len(current_batch_files) >= effective_batch_size or (i == len(files_to_process) - 1 and current_batch_files):
            if not current_batch_files:
                continue
                
            batch_num = get_next_batch_number()
            output_filename = f"{WATCHER_FILENAME_PREFIX}{batch_num}.yaml"
            output_path = os.path.join(OUTPUT_DIR, output_filename)
            
            output_data = {
                'metadata': {
                    'batch_number': batch_num,
                    'timestamp': datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    'hierarchy_rules': "Changes in SYMBOLS must be justified by objectives in REAL.",
                    'generated_by': os.path.basename(__file__),
                    'files_count': len(current_batch_files)
                },
                'watcher_validation_prompt': "Before writing any code, explain how these changes align with the 'real' objectives and how they will be verified in 'testing'.",
                'files': current_batch_files
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                yaml.dump(output_data, f, sort_keys=False, default_flow_style=False)
            
            print(f"\n>>> BATCH SAVED: {output_path} <<<")
            current_batch_files = [] 
            
            if create_sample:
                print("Sample created. Exiting.")
                break

            if i < len(files_to_process) - 1:
                cont = input("Batch saved. Continue to next batch? (Y/n): ").strip().lower()
                if cont == 'n':
                    break

def collect_feedback_yaml():
    """Wrapper for backwards compatibility"""
    collect_feedback_watcher()

if __name__ == "__main__":
    collect_feedback_yaml()
