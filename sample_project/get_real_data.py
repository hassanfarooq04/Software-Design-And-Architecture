import os
import ast
import json

def extract_real_data(root_folder):
    """
    Ye function real Python files parh karke Code aur Docstrings ka pair banata hai.
    """
    dataset = []
    
    # Folder mein saari files parhte hain
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith(".py"):
                filepath = os.path.join(dirpath, filename)
                
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        source_code = f.read()
                    
                    # Python AST Parser use karte hain
                    tree = ast.parse(source_code)
                    
                    # Tree mein se functions nikaalte hain
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            # Function ka naam
                            func_name = node.name
                            
                            # Docstring nikaalna (AST magic)
                            docstring = ast.get_docstring(node)
                            
                            # Agar docstring exist karti hai aur lambi hai
                            if docstring and len(docstring.strip()) > 20:
                                # Code chunk banao (Function signature + body)
                                # (Full code lamba hota hai, isliye sirf top lines le le rahe hain)
                                code_lines = source_code.split('\n')
                                func_start_line = node.lineno - 1
                                func_end_line = node.end_lineno if node.end_lineno else func_start_line + 5
                                
                                # Sirf code ka first part (snippet)
                                code_snippet = "\n".join(code_lines[func_start_line:func_end_line])
                                
                                dataset.append({
                                    "code": code_snippet,
                                    "documentation": docstring.strip(),
                                    "context": {
                                        "imports": [], # Import logic complex hai, abhi simplified
                                        "class_name": None,
                                        "package": os.path.basename(root_folder)
                                    }
                                })
                                    
                except Exception as e:
                    print(f"⚠️ File {filename} parse nahi hui: {e}")

    return dataset

# --- USAGE ---
# Yahan apne Local Project folder ka path dein
# Example: D:\MyPythonProject ya /content/sample_repo (Colab mein)
source_folder = r"/content/sample_project" # AGAR LOCAL PAR USE KAR RAHE HO TO PATH BADAL LEIN

print("🔍 Real Data Extraction Shuru...")
real_data = extract_real_data(source_folder)

# Save to Train Data File
with open("train_data.json", "w", encoding="utf-8") as f:
    json.dump(real_data, f, indent=4, ensure_ascii=False)

print(f"✅ Total {len(real_data)} real code-doc pairs collected!")
print("✅ File saved to train_data.json")