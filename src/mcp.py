from canvas.canvas import Slide
from dataclasses import dataclass, field
from typing import Any
from utils import *
from voice_model import TTSModel

@dataclass
class Function:
    function:str
    args:list

@dataclass
class Paragraph:
    text: str
    alignment: str = "left"  # can be "left", "middle", or "right"

@dataclass
class SlideData:
    title:Paragraph
    content: list[Any]

# change for each change in the yaml file
def StoreSlides(data) -> list[SlideData]:
    slides = data.get("slides",None)
    if len(slides) == 0:
        print("GetSlidesFromJson: no slides found in json")
        exit(1)

    slides_data: list[SlideData] = []
    for slide in slides:
        title = slide.get("title",())
        content = slide.get("content",())
        slides_data.append(SlideData(
            title= Paragraph(text=title["text"], alignment=title["alignment"]),
            content=content
        ))
        
    return slides_data

# makes tts from slidedata object that has all the yaml output
def MakeTranscripts(slide_data:SlideData):
    tts = TTSModel()
    text_for_transcript = ""
    slide_name = slide_data.title.text
    for item in slide_data.content:
        name = item.get("type","")
        args = item.get("args",[])
        
        if name == "text":
            txt = args.get("text","text missing")
            text_for_transcript = txt + " "
            
    tts.SpeakAndSave(text_for_transcript, slide_name)

# make slides from slidedata object that has all the yaml output
def MakeSlide(slide_data:SlideData):
    slide = Slide(slide_data.title.text)
    slide.AddTitleText(x=slide_data.title.alignment, text=slide_data.title.text)

    for item in slide_data.content:
        name = item.get("type","")
        args = item.get("args",[])
        
        if name == "text":
            txt = args.get("text","text missing")
            slide.AddBodyText(
                args.get("alignment","left"),
                text=args.get("text","text missing")
                )
            
        elif name == "plot_graph":
            slide.AddGraph(
                x = args.get("alignment","right"),
                points=args.get("points",(0,0)),
                x_label=args.get("x_label","x"),
                y_label=args.get("y_label","y"),
                title=args.get("title","graph"),
                scale=args.get("scale",1.0)
            )
        
        elif name == "render_latex":
            slide.AddLatexText(
                x = args.get("alignment","right"),
                latex_string=args.get("latex_str",""),
                scale=args.get("scale",1.0)
            )
        
    slide.Save("slide_output/")
            
for slide in StoreSlides(ExtractYaml("slides.yaml")):
    MakeSlide(slide)
    MakeTranscripts(slide)