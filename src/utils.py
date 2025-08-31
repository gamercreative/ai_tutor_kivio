import json 
import yaml

audio_sr = 22050

def ExtractJson(path:str): 
    with open(path,"r") as f:
        json_str = f.read()
        
    data = json.loads(json_str)
    return data

def ExtractYaml(path: str):
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    return data

# get audio file duaration
def GetAudioDuration(audio):
    if audio is None:
        raise ValueError("Audio is None! Cannot compute duration")
    return len(audio)/ audio_sr