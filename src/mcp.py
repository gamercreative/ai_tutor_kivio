import json 
import yaml
from canvas.canvas import Slide
import os
from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class Paragraph:
    text: str
    alignment: str = "left"  # can be "left", "middle", or "right"

@dataclass
class ToolCall:
    function: str
    args: Dict[str,Any] = field(default_factory=dict)

@dataclass
class SlideData:
    title:Paragraph
    text:Paragraph
    tools: List[ToolCall] = field(default_factory=list)

def ExtractJson(path:str): 
    with open(path,"r") as f:
        json_str = f.read()
        
    data = json.loads(json_str)
    return data

def ExtractYaml(path: str):
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    return data

def StoreSlides(data) -> list[SlideData]:
    slides = data.get("slides",None)
    if len(slides) == 0:
        print("GetSlidesFromJson: no slides found in json")
        exit(1)

    slides_data: list[SlideData] = []
    for slide in slides:
        tool_list = [ToolCall(**tool) for tool in slide.get("tools",[])]
        title = slide.get("title",())
        body = slide.get("body",())
        slides_data.append(SlideData(
            title= Paragraph(text=title["text"], alignment=title["alignment"]),
            text= Paragraph(text =body["text"], alignment=body["alignment"]),
            tools = tool_list
            ))
        
    print(slides_data)
    print(len(slides_data))
    return slides_data

def MakeSlide(slide_data:SlideData):
    slide = Slide(slide_data.title.text)
    slide.AddTitleText(x=slide_data.title.alignment, text=slide_data.title.text)
    slide.AddBodyText(x=slide_data.text.alignment, text=slide_data.text.text)

    for tool in slide_data.tools:
        if not tool:
            continue
        if tool.function == "render_latex":
            slide.AddLatexText(
                x=tool.args.get("alignment", "middle"),
                latex_string=tool.args["latex_str"]
            )

        elif tool.function == "plot_graph":
            slide.AddGraph(
                x=tool.args.get("alignment", "middle"),
                points=tool.args["points"],
                x_label=tool.args.get("x_label",""),
                y_label=tool.args.get("y_label",""),
                title=tool.args.get("title",""),
                scale=tool.args.get("scale", 1.0)
            )

    slide.Save("output/")
            
for slide in StoreSlides(ExtractYaml("slides.yaml")):
    print(slide.title.text)
    MakeSlide(slide)