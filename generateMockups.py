"""

Title: app.py

Author: Mphatso Simbao

Description: Main Script to combine designs and generate a bunch of shirt mockups

"""
#Import modules
import os
import random
from PIL import Image, ImageChops
from blendFunctions import Multiply,Difference,Normal


def GenerateFinalImage(designNumber,tempNumber,designIndex,design,template,productType):
    """_summary_

    Args:
        designNumber (_type_): _description_
        tempNumber (_type_): _description_
        designIndex (_type_): _description_
        design (_type_): _description_
        template (_type_): _description_
    """

    designMask = Image.new('RGBA', template.size, (0, 0, 0, 0))

    if (tempNumber == 2) and (productType=="shirts"):
        design = design.rotate(10)
        designMask.paste(design, (int((template.size[0] / 2) - (design.size[0] / 2))+100, 520), design.convert('RGBA'))
    else:
        designMask.paste(design, (int((template.size[0] / 2) - (design.size[0] / 2)), 500), design.convert('RGBA'))

    template = template.convert('RGBA')

    if (tempNumber == 3) or (tempNumber == 4):
        finalImage = Multiply(template,designMask).convert('RGB')
        if(designNumber == 1) or (designNumber == 6) or (designNumber == 7):
            finalImage = Difference(template, designMask).convert('RGB')
    else:
        finalImage = Normal(template, designMask).convert('RGB')

    finalImage.save('public/output/'+str(designIndex)+'1.jpg')


#Setup Defaults
def generateAllImages(designIndex,templateIndex,colorIndex,productType):

    #Define Variables
    designsDirectory = 'public/designs'
    defaultsDirectory = 'templates/defaults'

    templateDirectory = 'templates/'+productType
    colorsDirectory = 'templates/'+productType+'Colors'

    #Grab Designs
    designIndex = 0
    designFiles = os.listdir(designsDirectory)

    #Grab Templates
    templateIndex = 0
    templateFiles = os.listdir(templateDirectory)

    #Grab Shirt colors
    colorIndex = 0
    colorFiles = os.listdir(colorsDirectory)

    while designIndex < len(designFiles):

        designFilename = designFiles[designIndex]
        design = Image.open(designsDirectory + "/" + designFilename)
        designNumber = int(designFilename[0])

        templateFilename = templateFiles[templateIndex]
        template = Image.open(templateDirectory + "/" + templateFilename)
        tempNumber = int(templateFilename[0])

        #Make Default Template Image
        # if(designNumber == 2):
        #     print("Skip This")
        # else:
        defaultTemplate = Image.open(defaultsDirectory + "/" + productType + ".jpg")
        defaultTemplate.paste(design, (int((defaultTemplate.size[0] / 2) - (design.size[0] / 2)), 500), design.convert('RGBA'))
        defaultTemplate.save('public/output/'+str(designIndex)+'0.jpg')

        #Make Another Image Given a New Template

        GenerateFinalImage(designNumber,tempNumber,designIndex,design, template,productType)

        #Generate Flat Images to Show different shirt colors
        while colorIndex < len(colorFiles):
            colorFileName = colorFiles[colorIndex]
            color = Image.open(colorsDirectory + "/" + colorFileName)
            colorNumber = int(colorFileName[0])

            color = color.convert('RGBA')

            colorMask = Image.new('RGBA', color.size, (0, 0, 0, 0))

            if productType=="shirts":
                if (colorNumber == 5):
                    design = design.rotate(10)
                else:
                    design = design.rotate(8)
            else:
                if ((colorNumber == 3) or (colorNumber == 2)):
                    design = design.rotate(-8)
                else:
                    design = design.rotate(-12)


            wiggle = random.randint(0, 9)

            if productType == "shirts":
                colorMask.paste(design,(int((color.size[0] / 2) - (design.size[0] / 2))+wiggle,int((colorMask.size[1] / 2) - (design.size[1] / 2))+wiggle),design.convert('RGBA'))
            else:
                colorMask.paste(design,(int((color.size[0] / 2) - (design.size[0] / 2))-75,int((colorMask.size[1] / 2) - (design.size[1] / 2))+700),design.convert('RGBA'))

            #Steps to Create New Folded Sweater Mask'
            if productType == "sweatshirts":
                protoMask = Image.new('RGBA', color.size, (0, 0, 0, 0))
                imageMask = Image.open('templates/masks/'+str(colorNumber)+'.png').convert('L').resize(color.size)
                finalMask = Image.composite(colorMask,protoMask,imageMask)
                colorMask = finalMask
            #Use Final Mask instead of Color Mask

            if (colorNumber == 3) or (colorNumber == 4):
                finalImage = Multiply(color,colorMask).convert('RGB')
                if(designNumber == 1) or (designNumber == 6) or (designNumber == 7):
                    finalImage = Difference(color, colorMask).convert('RGB')
            else:
                finalImage = Normal(color, colorMask).convert('RGB')

            if productType=="shirts":
                if (colorNumber == 5):
                    design = design.rotate(-10)
                else:
                    design = design.rotate(-8)
            else:
                if ((colorNumber == 3) or (colorNumber == 2)):
                    design = design.rotate(8)
                else:
                    design = design.rotate(12)

            finalImage.save('public/output/'+str(designIndex) + str(colorIndex+2) + '.jpg')

            colorIndex += 1

        colorIndex = 0


        if(templateIndex == 2):
            templateIndex=0
        else:
            templateIndex+=1

        designIndex+=1

