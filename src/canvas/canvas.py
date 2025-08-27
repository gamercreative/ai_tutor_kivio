from PIL import Image,ImageDraw, ImageFont
from utils import WrapText, GetX
import matplotlib.pyplot as plt
import io

# a class for each slide containing the ability to just add to a slide using a function
class Slide:
    # takes res w x h and the color in plain text in rgb mode
    def __init__(self,slide_name:str, width:int=1280, height:int=720 , color:str="white"):
        # image file settings
        self.name = slide_name
        self.file_extension = ".png"
        
        # view port for image settings
        self.width= width
        self.height = height
        self.color = color
        
        #wraped text settings
        self.text_padding = 50
        self.line_spacing = 5
        
        # fonts can be customj or default
        try:
            self.title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size=48)
            print("title font found")
        except:
            print("No title font found, using default")
            self.title_font = ImageFont.load_default()

        try:
            self.body_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size=32)
            print("body font found")
        except:
            print("No body font found, using default")
            self.body_font = ImageFont.load_default()
            
        # cache
        self.last_cursor_y = 50
                
        # init sequence for canvas
        self.CreateEmptyImage()
        print("slide init completed")
            
    # creates an image
    def CreateEmptyImage(self):
        # now creates the image
        # saves the image as an object not saved to disk yet only ram
        self.img = Image.new("RGB",(self.width, self.height), color=self.color)
        # also saves a drawing context of the image to edit it
        self.draw = ImageDraw.Draw(self.img)
        print("image created successfuly")
                
    # adds text in the image in absoulte values
    def AddText(self, x:int, y:int=None, text:str= "", color:str = "black", font=None):
        # check if it overlaps
        if y is None or y <= self.last_cursor_y:
            y = self.last_cursor_y + self.line_spacing  # place below last object
        if not text:
            print("AddText: no intput text provided")
            
        self.draw.text((x,y),text, fill=color, font=font)
        print(f"{text} added at pos x:{x} y:y{y}")
        
        y = int(y) + self.line_spacing
        self.last_cursor_y = y

        
    # a wrapper for the image save to save to disk
    # path is without file name and extension only folder path
    def Save(self, path=""):
        path_with_file = path + self.name + self.file_extension
        self.img.save(path_with_file)
        print(f"saved file at {path_with_file}")

    # adds wraped text to the image
    def AddWrapedText(self, x:int, y:int=None, text:str = "", color:str = "black", max_width:int = None, font = None):
        # check if it overlaps
        if y is None or y <= self.last_cursor_y:
            y = self.last_cursor_y + self.line_spacing  # place below last object
        if not text:
            print("AddWrapedText: no intput text provided")
        
            
        max_width = self.width - self.text_padding
        lines = WrapText(draw_viewer=self.draw, text=text, font=font, max_width=max_width)
        if len(lines) == 0:
            print("AddWrapedText: wraptext returnd a list of length 0")
        
        cursur_y:int = y
        for line in lines:
            self.AddText(x=x , y=cursur_y, text=line, color=color, font=font)
            _, h = self.draw.textbbox((0, 0), line, font=font)[2:4]
            cursur_y += int(h) + self.line_spacing
            if cursur_y >= self.height:
                print("AddWrapedText: text is too big to fit in the frame")
                break
        self.last_cursor_y = cursur_y

    # just wrappers so no need for check and such things
    # add title text
    def AddTitleText(self, x, y:int=None, text:str = "", color:str = "black", max_width:int = None):
        x = GetX(self.width,x)
        slide.AddWrapedText(x, y, text, color, max_width, font=self.title_font)
        
    # add body text
    def AddBodyText(self, x, y:int=None, text:str = "", color:str = "black", max_width:int = None):
        x = GetX(self.width,x)
        slide.AddWrapedText(x, y, text, color, max_width, font=self.body_font)
        
    # adds a equation or so into the image
    def AddLatexText(self, x, y:int = None, latex_string:str = "", scale:float = 1.0):
        # check if it overlaps
        if y is None or y <= self.last_cursor_y:
            y = self.last_cursor_y + self.line_spacing
        if not latex_string:
            print("AddLatexText: no intput text provided")
        x = GetX(self.width,x)

        # try used for all as if a invalid input for the matplotlib will throw a big error somewhere
        try:
            fig, ax = plt.subplots(figsize=(4*scale, 1*scale), dpi=150)
            ax.axis("off")
            ax.text(0.5,0.5, f"${latex_string}$", fontsize=int(20*scale), ha="center", va = "center")
            buf = io.BytesIO()
            plt.savefig(buf, format="png", bbox_inches="tight", transparent=True)
            plt.close(fig)
            buf.seek(0)
            latex_img = Image.open(buf)
            self.img.paste(latex_img, (x,y), latex_img)
            self.last_cursor_y = y + latex_img.height + self.line_spacing

        except Exception as e:
            print(f"AddLatexText error: {e}")
    
title = "### RULES FOR GENERATION"
    
body = """
1. **JSON only**. Do not include markdown, comments, backticks, or text outside the JSON object.
2. `"title"` → Short, descriptive slide title.
3. `"text"` → Transcript for TTS, natural spoken style. At least 20 words if only text. Max 50 words (60 if multiple tools).
4. `"tools"` → Each slide can include at most 1 `render_latex` and 1 `plot_graph` entry.
"""

slide = Slide("akram")
slide.AddTitleText("middle", text=title)
slide.AddBodyText("left", text=body)
slide.AddLatexText("left", latex_string="c^2 = a^2 + b^2", scale=1.5)
slide.AddBodyText("left", text="test 2")
slide.Save()