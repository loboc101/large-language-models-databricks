# Databricks notebook source
# %pip install transformers

# COMMAND ----------

# Step 1: Imports
import os
import json
import requests
from transformers import pipeline

# Step 2: Initialize SparkSession (Databricks handles this, but we'll leave it for local environments)
# spark = SparkSession.builder \
#     .appName("LLM-Generic-Databricks") \
#     .getOrCreate()

# Step 3: Create directories or set up necessary environment
dbutils.fs.mkdirs("/mnt/large-language-models")

# Step 4: Load data (adjust paths accordingly)
input_data_path = "/mnt/large-language-models/data.csv"  # Databricks DBFS path
if not dbutils.fs.ls("/mnt/large-language-models"): dbutils.fs.put(input_data_path, 'col1,col2\nval1,val2\nval3,val4', overwrite=True)

# Step 5: Initialize a text generation pipeline
generator = pipeline("text-generation", model="gpt2")

# Step 6: Use the model (example)
text_prompt = "Once upon a time"
output = generator(text_prompt, max_length=50)
print(output)

# Step 7: Save the output to DBFS
output_path = "/mnt/large-language-models/output"
df = spark.createDataFrame(output)
df.write.format("csv").save(output_path)

# Clean up SparkSession (Databricks usually handles this, but good practice for local runs)
# spark.stop()

# COMMAND ----------

dbutils.fs.ls("/mnt/large-language-models")
