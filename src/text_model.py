import matplotlib.pyplot as plt
import yaml
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from os import makedirs

class TextModel:
    def __init__(self,path = "text_output"):
        self.model_id = "alokabhishek/Mistral-7B-Instruct-v0.2-bnb-4bit"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id, use_fast=True)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_id, device_map="auto")
        self.pipe = pipeline(model=self.model, tokenizer=self.tokenizer, task='text-generation')
        self.format = "json" # can be "yaml"
        makedirs(path,exist_ok = True)
        self.output_dest = path.strip() + "/" + f"slides.{self.format}"

    def GetPrompt(self,path = "prompts/prompt.txt",topic=""):
        with open(path, "r") as f:
            prompt_template = f.read()
        return prompt_template.replace("<Topic>",topic)

    def GetRag(self,path = "rag_docs/pythag.txt"):
        with open(path, "r") as f:
            rag_data = f.read()

    def GenerateText(self,topic):
        prompt = self.GetPrompt(topic=topic)
        
        rag = self.GetRag()
        # prompt = prompt_template.replace("<RAG>", rag_data)
        
        # get output and filter the output text form the rest of hte metadat
        output = self.pipe(prompt, max_new_tokens=4000, return_full_text=False, temperature= 0.05)
        slides = output[0]["generated_text"]
        
        self.Save(slides)
        return self.output_dest

    # Save the output as a YAML file
    def Save(self, slides):
        with open(self.output_dest, "w") as f:
            f.write(slides)
            print("done")

        try:
            slides_data = yaml.safe_load(slides)
        except yaml.YAMLError as e:
            print("YAML parsing error:", e)
            slides_data = None

