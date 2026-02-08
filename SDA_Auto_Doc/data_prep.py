import ast
import json
import random

def generate_dummy_data(num_samples=100):
    """
    Generates dummy Python code-documentation pairs for training.
    In a real scenario, this would use Tree-sitter to scrape GitHub.
    """
    data = []
    
    code_templates = [
        ("def calculate_sum(a, b):", "return a + b", "Calculates the sum of two numbers."),
        ("def fetch_user_data(user_id):", "return db.query(user_id)", "Fetches user details from the database."),
        ("def process_image(image):", "return image.resize(128, 128)", "Resizes the input image to 128x128 pixels."),
        ("def validate_email(email):", "return '@' in email", "Checks if the string contains a valid email format."),
        ("def save_log(message):", "file.write(message)", "Appends a log message to the log file.")
    ]
    
    for i in range(num_samples):
        # Select random template
        sig, body, desc = random.choice(code_templates)
        
        # Create a Python AST object
        code_str = f"{sig}\n    {body}\n"
        
        # Create a "docstring" style label
        docstring = f'"""{desc}"""'
        
        # Context enrichment (simulated)
        imports = ["import random", "import os"]
        
        data.append({
            "code": code_str,
            "documentation": docstring,
            "context": {
                "imports": imports,
                "class_name": None,
                "package": "utils"
            }
        })
    
    # Save to JSON
    with open("train_data.json", "w") as f:
        json.dump(data, f, indent=4)
    
    print(f"✅ Generated {num_samples} samples and saved to train_data.json")

if __name__ == "__main__":
    generate_dummy_data(500) # Generate 500 training examples