import math
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import io
import yaml
import os
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

model_id = "alokabhishek/Mistral-7B-Instruct-v0.2-bnb-4bit"
tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=True)
model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto")

pipe = pipeline(model=model, tokenizer=tokenizer, task='text-generation')

# -------------------------
# 2️⃣ Load prompt and RAG
# -------------------------
with open("prompts/prompt.txt", "r") as f:
    prompt_template = f.read()

with open("rag_docs/pythag.txt", "r") as f:
    rag_data = f.read()

# Inject RAG into the prompt
prompt = prompt_template.replace("<RAG>", rag_data)

# get output and filter the output text form the rest of hte metadat
output = pipe(prompt, max_new_tokens=1500, return_full_text=False)
slides_yaml = output[0]["generated_text"]

try:
    slides_data = yaml.safe_load(slides_yaml)
except yaml.YAMLError as e:
    print("YAML parsing error:", e)
    slides_data = None

# Save the output as a YAML file
with open("slides.yaml", "w") as f:
    f.write(slides_yaml)
    print("done")