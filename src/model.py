import json
import math
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import io
import os
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

model_id = "alokabhishek/Mistral-7B-Instruct-v0.2-bnb-4bit"
tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=True)
model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto")

pipe = pipeline(model=model, tokenizer=tokenizer, task='text-generation')

# -------------------------
# 2️⃣ Load prompt and RAG
# -------------------------
with open("prompts/prompt2.txt", "r") as f:
    prompt_template = f.read()

with open("rag_docs/pythag.txt", "r") as f:
    rag_data = f.read()

# Inject RAG into the prompt
prompt = prompt_template.replace("<RAG>", rag_data)

# get output and filter the output text form the rest of hte metadat
output = pipe(prompt, max_new_tokens=1500, return_full_text=False)
slides_json = output[0]["generated_text"]

# filter anything except for the json response if anyting else exists
first_brace = slides_json.find("{")
if first_brace != -1:
    slides_json_clean = slides_json[first_brace:]
else:
    raise ValueError("No JSON object found in the model output")

# save the output 
with open("../slides.json", "w") as f:
    f.write(slides_json_clean)