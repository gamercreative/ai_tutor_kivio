from PIL import Image,ImageDraw, ImageFont
from canvas.utils import WrapText, GetX
import matplotlib.pyplot as plt
import io
from os import makedirs
from pylatexenc.latexwalker import LatexWalker
from pylatexenc.latex2text import LatexNodes2Text
import math # remove ba3ed el testing

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
        self.line_spacing = 12
        
        # fonts can be customj or default
        try:
            self.title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size=48)
        except:
            print("No title font found, using default")
            self.title_font = ImageFont.load_default()

        try:
            self.body_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size=32)
        except:
            print("No body font found, using default")
            self.body_font = ImageFont.load_default()
            
        # cache
        self.last_cursor_y = 50
                
        # init sequence for canvas
        self.CreateEmptyImage()
            
    # creates an image
    def CreateEmptyImage(self):
        # now creates the image
        # saves the image as an object not saved to disk yet only ram
        try:
            self.img = Image.new("RGB",(self.width, self.height), color=self.color)
            # also saves a drawing context of the image to edit it
            self.draw = ImageDraw.Draw(self.img)
        except Exception as e:
            print(f"CreateEmptyImage: {e}")
                
    # adds text in the image in absoulte values
    def AddText(self, x:int, y:int=None, text:str= "", color:str = "black", font=None):
        # check if it overlaps
        if y is None or y <= self.last_cursor_y:
            y = self.last_cursor_y + self.line_spacing  # place below last object
        if not text:
            print("AddText: no intput text provided")
            
        # Parse the LaTeX code
        latex_walker = LatexWalker(text)
        nodelist, pos, len_consumed = latex_walker.get_latex_nodes()

        # Convert to plain text with Unicode math symbols
        unicode_text = LatexNodes2Text().nodelist_to_text(nodelist)
            
        self.draw.text((x,y),text, fill=color, font=font)
        # print(f"{text} added at pos x:{x} y:y{y}")
        
        y = int(y) + self.line_spacing
        self.last_cursor_y = y

        
    # a wrapper for the image save to save to disk
    # path is without file name and extension only folder path
    def Save(self, path=""):
        makedirs(name=path, exist_ok = True)
        path_with_file = path + self.name + self.file_extension
        self.img.save(path_with_file)
        print(f"saved file at {path_with_file}")

    # adds wraped text to the image
    def AddWrapedText(self, x, y:int=None, text:str = "", color:str = "black", max_width:int = None, font = None):
        # check if it overlaps
        if y is None or y <= self.last_cursor_y:
            y = self.last_cursor_y + self.line_spacing  # place below last object
        if not text:
            print("AddWrapedText: no intput text provided")
        if y >= self.height:
            print("AddWrapedText: slide cannot fit more content vertically")
        
            
        max_width = self.width - self.text_padding
        lines = WrapText(draw_viewer=self.draw, text=text, font=font, max_width=max_width)
        if len(lines) == 0:
            print("AddWrapedText: wraptext returnd a list of length 0")
        
        cursur_y:int = y
        for line in lines:
            w, h = self.draw.textbbox((0, 0), line, font=font)[2:4]
            x_new = GetX(self.width,x,int(w))
            self.AddText(x=x_new , y=cursur_y, text=line, color=color, font=font)
            cursur_y += int(h) + self.line_spacing
            if cursur_y >= self.height:
                print("AddWrapedText: text is too big to fit in the slide frame")
                break
        self.last_cursor_y = cursur_y

    # just wrappers so no need for check and such things
    # add title text
    def AddTitleText(self, x, y:int=None, text:str = "", color:str = "black", max_width:int = None):
        self.AddWrapedText(x, y, text, color, max_width, font=self.title_font)
        
    # add body text
    def AddBodyText(self, x, y:int=None, text:str = "", color:str = "black", max_width:int = None):
        self.AddWrapedText(x, y, text, color, max_width, font=self.body_font)
        
    # adds a equation or so into the image
    def AddLatexText(self, x, y:int = None, latex_string:str = "", scale:float = 1.0):
        # check if it overlaps
        if y is None or y <= self.last_cursor_y:
            y = self.last_cursor_y + self.line_spacing
        if not latex_string:
            print("AddLatexText: no intput text provided")
        if y >= self.height:
            print("AddWrapedText: slide cannot fit more content vertically")

        # try used for all as if a invalid input for the matplotlib will throw a big error somewhere
        try:
            fig, ax = plt.subplots(figsize=(4*scale, 1*scale), dpi=150)
            ax.axis("off")
            ax.text(0.5,0.5, f"${latex_string}$", fontsize=int(20*scale), ha="center", va = "center")
            
            # savign to buffer not to disk
            # if ram is overused or bad performence save to disk and bitch
            buf = io.BytesIO()
            plt.savefig(buf, format="png", bbox_inches="tight", transparent=True)
            plt.close(fig)
            buf.seek(0)
            latex_img = Image.open(buf)
            
            x = GetX(self.width,x ,latex_img.width)
            self.img.paste(latex_img, (x,y), latex_img)
            self.last_cursor_y = y + latex_img.height + self.line_spacing

        except Exception as e:
            print(f"AddLatexText error: {e}")
            
    # adds a graph of any kind to the slide
    def AddGraph(self, x, y:int = None, points:list = None, x_label:str = None, y_label:str = None, title:str = None, scale:float = 1.0):
        # check if it overlaps
        if y is None or y <= self.last_cursor_y:
            y = self.last_cursor_y + self.line_spacing
        if len(points) == 0:
            print("AddGraph: no intput points provided")
        if y >= self.height:
            print("AddWrapedText: slide cannot fit more content vertically")

        try:
            fig,ax = plt.subplots(figsize=(2*scale, 1*scale),dpi = 150)
            xs,ys = zip(*points)
            ax.plot(xs,ys,marker="o",linestyle="-")
            
            if title: ax.set_title(label=title)
            else: print("AddGraph: not title provided for the graph")
            
            if x_label: ax.set_xlabel(xlabel=x_label)
            else: print(f"AddGraph: no x label provided for graph {title}")
            
            if y_label: ax.set_ylabel(ylabel=y_label)
            else: print(f"AddGraph: no y label provided for graph {title}")
            
            buf = io.BytesIO()
            plt.savefig(buf,format="png",bbox_inches="tight",transparent = True)
            plt.close(fig)
            buf.seek(0)
            graph_image = Image.open(buf)
            
            x = GetX(self.width,x ,graph_image.width)
            self.img.paste(graph_image, (x, y), graph_image)
            self.last_cursor_y = y + graph_image.height + self.line_spacing
            
        except Exception as e:
                print(f"AddGraph error: {e}")

if __name__ == "__main__":
    title = "Quadratic Growth Function"
        
    body = """
    This graph shows a quadratic growth function, where the y values increase as the square of x. Notice how the curve starts shallow and then rises sharply. Quadratic functions model acceleration, projectile motion, and many natural growth processes.
    """

    points = [(x, math.sin(x/2) * 10) for x in range(0, 50)]

    slide = Slide("akram")
    slide.AddTitleText("middle", text=title)
    slide.AddBodyText("left", text=body)
    # slide.AddLatexText("middle", latex_string="c^2 = a^2 + b^2", scale=1)
    slide.AddGraph("middle", points=points, x_label="X", y_label="Y", title="Quadratic Growth", scale=2)
    slide.Save()