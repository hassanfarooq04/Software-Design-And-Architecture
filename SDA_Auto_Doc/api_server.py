from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from peft import PeftModel
import time

app = FastAPI(title="Auto-Documentation API")

# Load Base Model
BASE_MODEL_ID = "meta-llama/Meta-Llama-3.1-8B-Instruct"
ADAPTER_PATH = "./llama-docs-finetuned" # Path where train.py saved model

print("📥 Loading Fine-Tuned Model...")
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_ID)
tokenizer.pad_token = tokenizer.eos_token

base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL_ID,
    torch_dtype=torch.float16,
    device_map="auto",
    load_in_4bit=True
)

# Load LoRA Adapters
model = PeftModel.from_pretrained(base_model, ADAPTER_PATH)
print("✅ Model Loaded!")

# Request Models
class DocRequest(BaseModel):
    code: str
    language: str = "python"

@app.post("/generate")
def generate_documentation(req: DocRequest):
    start_time = time.time()
    
    # Format Prompt
    prompt = f"""You are an expert software documentation generator.
    
Code:
{req.code}

Generate comprehensive documentation:

Documentation:"""

    try:
        # Tokenize
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        
        # Generate
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=150,
                temperature=0.7,
                do_sample=True,
                top_p=0.95,
                repetition_penalty=1.1
            )
        
        # Decode
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract result (simple string splitting)
        if "Documentation:" in generated_text:
            result = generated_text.split("Documentation:")[1].strip()
        else:
            result = generated_text.strip()

        latency = time.time() - start_time
        
        return {
            "documentation": result,
            "latency_seconds": round(latency, 2)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run Command: uvicorn api_server:app --host 0.0.0.0 --port 8000