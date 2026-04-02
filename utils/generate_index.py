import os
import json
import re

# Path to the data folder (relative to script location)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SCRIPT_DIR, "..", "data")
OUTPUT_PATH = os.path.join(DATA_PATH, "index.json")

# Language mapping (extract language name before underscore/date)
def extract_language(filename):
    """Extract language name from filename like cpp_cot.jsonl, python_2025-04-06.jsonl, etc."""
    # Remove .jsonl extension
    name = filename.replace('.jsonl', '')
    
    # Extract language (before underscore or date pattern)
    match = re.match(r'^([a-z]+)', name)
    if match:
        lang = match.group(1)
        # Handle special cases
        if lang == 'csharp':
            return 'csharp'
        elif lang == 'javascript':
            return 'javascript'
        elif lang == 'typescript':
            return 'typescript'
        return lang
    return None

def generate_index():
    """Generate index.json from data folder structure"""
    models = []
    
    # Get all directories in data folder
    try:
        items = sorted(os.listdir(DATA_PATH))
    except Exception as e:
        print(f"Error reading data folder: {e}")
        return
    
    for item in items:
        # # Skip files and folders starting with _old
        # if not os.path.isdir(os.path.join(DATA_PATH, item)) or item.startswith('_old'):
        #     continue
        
        model_path = os.path.join(DATA_PATH, item)
        
        # Get all .jsonl files in the folder (excluding meta.json)
        try:
            files = [f for f in os.listdir(model_path) 
                    if f.endswith('.jsonl') and f != 'meta.json']
        except Exception as e:
            print(f"Error reading folder {item}: {e}")
            continue
        
        if not files:
            print(f"Skipping {item}: no .jsonl files found")
            continue
        
        # Build files dictionary
        files_dict = {}
        for file in files:
            lang = extract_language(file)
            if lang:
                files_dict[lang] = file
        
        if files_dict:
            models.append({
                "name": item,
                "files": files_dict
            })
            print(f"Added model: {item} with {len(files_dict)} languages")
    
    # Sort models alphabetically
    models.sort(key=lambda x: x['name'])
    
    # Create final structure
    index = {"models": models}
    
    # Write to index.json
    try:
        with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)
        print(f"\nSuccessfully generated {OUTPUT_PATH}")
        print(f"Total models: {len(models)}")
    except Exception as e:
        print(f"Error writing index.json: {e}")

if __name__ == "__main__":
    generate_index()
