# Databricks notebook source
dbutils.fs.ls("/mnt/")

# COMMAND ----------

# Import necessary libraries
import os
from transformers import pipeline

# Optional: Install the required libraries on Databricks
# %pip install transformers

# Function to fetch model from Hugging Face and generate text
def generate_text_with_hugging_face(model_name: str, prompt: str, max_length: int = 50):
    # Load the pre-trained model from Hugging Face
    generator = pipeline("text-generation", model=model_name)
    
    # Generate text based on the provided prompt
    generated_text = generator(prompt, max_length=max_length)
    
    return generated_text

# Define the model name, prompt, and max length for text generation
model_name = "gpt2"
prompt = "Once upon a time in a far away land"
max_length = 100

# Generate text using the defined model and prompt
generated_output = generate_text_with_hugging_face(model_name, prompt, max_length)

# Print the generated output
print("Generated Text:")
for idx, output in enumerate(generated_output):
    print(f"{idx + 1}: {output['generated_text']}")

# Optionally save the generated output to DBFS or local storage
output_path = "/mnt/large-language-models/generated_text_output.txt"

# Create the directory if it doesn't exist
os.makedirs("/mnt/large-language-models", exist_ok=True)

# Save the generated output to a file
with open(output_path, "w") as file:
    for idx, output in enumerate(generated_output):
        file.write(f"{idx + 1}: {output['generated_text']}\n")

print(f"Output saved to {output_path}")
