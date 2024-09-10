# Databricks notebook source
# MAGIC %pip install PyPDF2 transformers

# COMMAND ----------

dbutils.fs.mkdirs("/mnt/tmp")

# COMMAND ----------

# Step 1: Install necessary libraries
# %pip install PyPDF2 transformers

import requests
from PyPDF2 import PdfReader
from transformers import pipeline

# Step 2: Download a sample PDF file from the internet
pdf_url = "https://arxiv.org/pdf/2203.15556.pdf"  # Example: Arxiv research paper
response = requests.get(pdf_url)

# Save the downloaded PDF to DBFS or a local path
# pdf_path = "/tmp/sample.pdf"  # For Databricks: Use DBFS path like "/dbfs/tmp/sample.pdf"
pdf_path = "/dbfs/mnt/tmp/sample.pdf"
with open(pdf_path, "wb") as file:
    file.write(response.content)

# Step 3: Extract text from the PDF
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Extract text from the downloaded PDF
extracted_text = extract_text_from_pdf(pdf_path)

# Return word count of the extracted text
def count_words(text):
    return len(text.split())
print(f"Word count: {count_words(extracted_text)}")

# Step 4: Summarize the extracted text using Hugging Face's text summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Summarize the text in chunks to avoid token length limitations
def summarize_text(text, max_chunk_length=1024):
    summaries = []
    for i in range(0, len(text), max_chunk_length):
        chunk = text[i:i + max_chunk_length]
        summary = summarizer(chunk, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
        summaries.append(summary)
    return " ".join(summaries)

# Generate summary of the extracted text
summary = summarize_text(extracted_text)

# Print the summary
print("Summary of the PDF:\n", summary)

# Step 5: Optionally, save the summary to a file in DBFS or local storage
summary_output_path = "/dbfs/mnt/large-language-models/summary_output.txt"
with open(summary_output_path, "w") as file:
    file.write(summary)

print(f"Summary saved to {summary_output_path}")

# COMMAND ----------

dbutils.fs.ls("/mnt/tmp/")

# COMMAND ----------

## Use a small model
# Step 1: Install necessary libraries
# %pip install PyPDF2 transformers

import requests
from PyPDF2 import PdfReader
from transformers import pipeline

# Step 2: Download a sample PDF file from the internet
pdf_url = "https://arxiv.org/pdf/2203.15556.pdf"  # Example: Arxiv research paper
response = requests.get(pdf_url)

# Save the downloaded PDF to DBFS or a local path
# pdf_path = "/tmp/sample.pdf"  # For Databricks: Use DBFS path like "/dbfs/tmp/sample.pdf"
pdf_path = "/dbfs/mnt/tmp/sample.pdf"
with open(pdf_path, "wb") as file:
    file.write(response.content)

# Step 3: Extract text from the PDF
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Extract text from the downloaded PDF
extracted_text = extract_text_from_pdf(pdf_path)

# Return word count of the extracted text
def count_words(text):
    return len(text.split())
print(f"Word count: {count_words(extracted_text)}")

# Step 4: Summarize the extracted text using Hugging Face's text summarization pipeline
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# Summarize the text in chunks to avoid token length limitations
def summarize_text(text, max_chunk_length=1024):
    summaries = []
    for i in range(0, len(text), max_chunk_length):
        chunk = text[i:i + max_chunk_length]
        summary = summarizer(chunk, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
        summaries.append(summary)
    return " ".join(summaries)

# Generate summary of the extracted text
summary = summarize_text(extracted_text)

# Print the summary
print("Summary of the PDF:\n", summary)

# Step 5: Optionally, save the summary to a file in DBFS or local storage
summary_output_path = "/dbfs/mnt/large-language-models/summary_output.txt"
with open(summary_output_path, "w") as file:
    file.write(summary)

print(f"Summary saved to {summary_output_path}")

