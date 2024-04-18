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

productType = "sweatshirts"

designsDirectory = 'designs'

colorsDirectory = 'templates/'+productType+'Colors'
colorFiles = os.listdir(colorsDirectory)
colorFileName = '1.jpg'

design = Image.open("designs/3.png")
design = design.rotate(-12)

color = Image.open(colorsDirectory + '/' + colorFileName)
color = color.convert('RGBA')
colorMask = Image.new('RGBA', color.size, (0, 0, 0, 0))


colorMask.paste(design,(int((color.size[0] / 2) - (design.size[0] / 2))-75,int((colorMask.size[1] / 2) - (design.size[1] / 2))+700),design.convert('RGBA'))

#Steps to Create New Folded Sweater Mask
protoMask = Image.new('RGBA', color.size, (0, 0, 0, 0))
imageMask = Image.open('templates/sweatshirtsColors/masks/1.png').convert('L').resize(color.size)
finalMask = Image.composite(colorMask,protoMask,imageMask)
#Use Final Mask instead of Color Mask

finalImage = Normal(color, finalMask).convert('RGB')

finalImage.save('test.jpg')
