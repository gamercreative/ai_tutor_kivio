import json 
import yaml

def ExtractJson(path:str): 
    with open(path,"r") as f:
        json_str = f.read()
        
    data = json.loads(json_str)
    return data

def ExtractYaml(path: str):
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    return data