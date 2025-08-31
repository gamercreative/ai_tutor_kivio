from src.mcp import MakeVideo
from src.text_model import TextModel

text_path = TextModel().GenerateText()
MakeVideo(text_path)