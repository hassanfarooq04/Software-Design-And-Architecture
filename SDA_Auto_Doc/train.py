import json
import torch
from transformers import (
    AutoModelForCausalLM, 
    AutoTokenizer, 
    TrainingArguments, 
    Trainer, 
    DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model, TaskType
from torch.utils.data import Dataset

# Load Data
with open("train_data.json", "r") as f:
    raw_data = json.load(f)

# Prepare Dataset Class
class CodeDocDataset(Dataset):
    def __init__(self, data, tokenizer, max_length=512):
        self.data = data
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        
        # Format Prompt (As per your document)
        prompt = f"""You are an expert software documentation generator.

Context:
- Package: {item['context']['package']}
- Imports: {', '.join(item['context']['imports'])}

Code:
{item['code']}

Generate comprehensive documentation:

Documentation:
{item['documentation']}"""

        # Tokenize
        encodings = self.tokenizer(
            prompt,
            truncation=True,
            max_length=self.max_length,
            padding="max_length",
            return_tensors="pt"
        )

        return {
            "input_ids": encodings["input_ids"].flatten(),
            "attention_mask": encodings["attention_mask"].flatten(),
            # For causal LM, labels are same as input_ids
            "labels": encodings["input_ids"].flatten()
        }

# Load Model & Tokenizer
MODEL_NAME = "meta-llama/Meta-Llama-3.1-8B-Instruct" # Or "TinyLlama/TinyLlama-1.1B-Chat-v1.0" for testing

print("📥 Loading model...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
tokenizer.pad_token = tokenizer.eos_token

# Load model with 4-bit quantization (saves memory)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
    device_map="auto",
    load_in_4bit=True # Requires bitsandbytes
)

# LoRA Configuration (Exactly as in PDF)
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

# Prepare Data
dataset = CodeDocDataset(raw_data, tokenizer)
train_dataset, val_dataset = torch.utils.data.random_split(dataset, [0.9, 0.1])

# Training Arguments
training_args = TrainingArguments(
    output_dir="./llama-docs-finetuned",
    num_train_epochs=3, # Reduced for demo, PDF says 5
    per_device_train_batch_size=2, # Adjust based on GPU VRAM
    per_device_eval_batch_size=2,
    gradient_accumulation_steps=4,
    warmup_steps=100,
    logging_steps=10,
    save_steps=50,
    evaluation_strategy="steps",
    eval_steps=50,
    learning_rate=2e-4,
    fp16=True, # Use mixed precision
    report_to="none"
)

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False)
)

# Start Training
print("🚀 Starting Fine-Tuning...")
trainer.train()
print("✅ Training Complete! Model saved to ./llama-docs-finetuned")