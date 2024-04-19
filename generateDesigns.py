from PIL import Image, ImageDraw, ImageFont

# currentDesign = ["it's a","beautiful","day for","banjo"]
nectarinePalette=[(242,202,141,255),(247,187,153,255),(249,221,210,255),(225,183,208,255)]
marginPalette=[(185,92,42,255),(224,165,52,255),(167,185,148,255),(109,146,121,255)]

MAX_W, MAX_H = 1550, 2000

def generateDesign(designWords,outputNumber,font,style,palette,MAX_W,MAX_H):
    """_summary_

    Args:
        outputNumber (_type_): _description_
        font (_type_): _description_
        style (_type_): _description_
    """

    im = Image.new('RGBA', (MAX_W, MAX_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)

    if font == 'margin':
        current_h, pad = -140,215
    elif font == 'summer':
        current_h, pad = 200,215
    else:
        current_h, pad = 260, 260

    font_path="fonts/"+font+".ttf"

    imageFont = ImageFont.truetype(font_path, 288)
    fillIndex = 0

    match style:
        case "plain":
            for line in designWords:
                w = draw.textlength(line, font=imageFont)
                draw.text(( ((MAX_W - w) / 2)-70, current_h), line.upper(), font=imageFont)
                current_h += pad
        case "colorLine":
            for line in designWords:
                if font=="nectarine": line = line.upper()
                w = draw.textlength(line, font=imageFont)
                draw.text(((MAX_W - w) / 2, current_h), line, font=imageFont, fill=palette[fillIndex])
                current_h += pad
                if fillIndex==3:
                    fillIndex = 0
                else:
                    fillIndex += 1
        case "colorCharacter":
            for line in designWords:
                if font=="nectarine": line = line.upper()
                w = draw.textlength(line, font=imageFont)
                x = (MAX_W - w)/2
                for char in line:
                    if font=="nectarine": char = char.upper()
                    c = draw.textlength(char, font=imageFont)
                    draw.text( (x, current_h), char, font=imageFont, fill=palette[fillIndex])
                    x += c
                    if fillIndex==3:
                        fillIndex = 0
                    else:
                        fillIndex += 1

                current_h += pad

    im.save("public/designs/"+str(outputNumber)+".png")

def MakeAllDesigns(currentDesign):
    """_summary_

    Args:
        currentDesign (_type_): _description_
    """
    generateDesign(currentDesign,1,'summer','plain',None,1400,2000)
    generateDesign(currentDesign,2,'margin','colorLine',marginPalette,1550, 2000)
    generateDesign(currentDesign,3,'nectarine','colorLine',nectarinePalette,1550,2000)
    generateDesign(currentDesign,4,'margin','colorCharacter',marginPalette,1550,2000)
    generateDesign(currentDesign,5,'nectarine','colorCharacter',nectarinePalette,1550,2000)

# MakeAllDesigns(currentDesign)