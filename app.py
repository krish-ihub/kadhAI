import json
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("RajuKandasamy/tamillama_tiny_30m")
model = AutoModelForCausalLM.from_pretrained("RajuKandasamy/tamillama_tiny_30m")

# Define the prompt
prompt = f"""சொற்கள்:
வாக்குறுதி, எலி, பெரியது
சுருக்கம்:"""

# Tokenize the input prompt
input_ids = tokenizer(prompt, return_tensors="pt").input_ids

# Generate the output
generation_output = model.generate(input_ids=input_ids, max_new_tokens=256)

# Decode the generated output
output_text = tokenizer.decode(generation_output[0])

# Store the output in a JSON file
output_data = {
    "prompt": prompt, \
    
    "generated_text": output_text
}

# Save the data as a JSON file
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(output_data, f, ensure_ascii=False, indent=4)

print("Output stored in output.json")
