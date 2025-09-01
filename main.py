from src.mcp import MakeVideo
from src.text_model import TextModel

topic = input("enter your video idea here: ")
text_path = TextModel().GenerateText(topic)
MakeVideo(text_path)

# MakeVideo("text_output/slides.yaml")