def WrapText(draw_viewer, text, font, max_width):
    words = text.split()
    lines = []
    cur_line = ""
    
    for word in words:
        # if there is a word and not eos then add the word
        # to the test line to check if out of bounds
        test_line = cur_line + (" " if cur_line else "") + word
        
        # get bouding box
        bbox = draw_viewer.textbbox((0,0),test_line, font=font)
        w = bbox[2] - bbox[0]
        
        # check if the test_line is short enough for max width
        # if it is shorter than test_line then make it curret best line
        if w <= max_width:
            cur_line = test_line
        
        # if its bigger then the cur_line is the limit and use that
        else:
            if cur_line:
                lines.append(cur_line)
                cur_line = word
    if cur_line:
        lines.append(cur_line)
    
    return lines

def GetX(width:int, placement:str):
    horizental_padding = 50
    
    if placement == "middle":
        return int(width/2)
    
    if placement == "left":
        return int(horizental_padding)
    
    if placement == "right":
        return int(width-horizental_padding)
    
    return 50