import os
from flask import Flask, render_template, request
from dotenv import set_key, load_dotenv
from pathlib import Path
import generateDesigns as generateDesigns
import generateMockups

load_dotenv()

env_file_path = Path(".env")
# Create the file if it does not exist.
# env_file_path.touch(mode=0o600, exist_ok=False)
# Save some values to the file.
# set_key(dotenv_path=env_file_path, key_to_set="USERNAME", value_to_set="John")
# set_key(dotenv_path=env_file_path, key_to_set="EMAIL", value_to_set="abc@gmail.com")

#TODO
#Figure out sections
#switch designs to input form edit system

#add button for generate designs

#add buttons for generate shirt images
#add button for preview shirt images
#add button for publish shirt images

#do all this for sweatshirts too
design_line1=os.getenv('DESIGN_LINE1')
design_line2=os.getenv('DESIGN_LINE2')
design_line3=os.getenv('DESIGN_LINE3')
design_line4=os.getenv('DESIGN_LINE4')

title=os.getenv('TITLE')
tags=os.getenv('TAGS')
section=os.getenv('SECTION')

#Define Variables for Current Design
name = 'Mphatso'

#Generate Authentication Link
client_id=os.getenv('KEYSTRING')
state=os.getenv('STATE')
code_challenge=os.getenv('CODE_CHALLENGE')
auth_link = "https://www.etsy.com/oauth/connect?response_type=code&redirect_uri=http://localhost:3003/oauth/redirect&scope=email_r%20listings_r%20listings_w%20shops_r%20shops_w&client_id="+client_id+"&state="+state+"&code_challenge="+code_challenge+"&code_challenge_method=S256"

app = Flask(__name__, static_folder='public', template_folder='views')

@app.route("/")
def index():

    design_line1=os.getenv('DESIGN_LINE1')
    design_line2=os.getenv('DESIGN_LINE2')
    design_line3=os.getenv('DESIGN_LINE3')
    design_line4=os.getenv('DESIGN_LINE4')

    title=os.getenv('TITLE')
    tags=os.getenv('TAGS')
    section=os.getenv('SECTION')
    return render_template('index.html',
                           name=name,
                           auth_link=auth_link,
                           design_line1=design_line1,
                           design_line2=design_line2,
                           design_line3=design_line3,
                           design_line4=design_line4,
                           title=title,
                           tags=tags
                           )

@app.route('/read-form', methods=['POST']) 
def read_form(): 
  
    # Get the form data as Python ImmutableDict datatype  
    data = request.form 
  
    ## Return the extracted information  
    set_key(dotenv_path=env_file_path, key_to_set="DESIGN_LINE1", value_to_set=data['design_line1'])
    set_key(dotenv_path=env_file_path, key_to_set="DESIGN_LINE2", value_to_set=data['design_line2'])
    set_key(dotenv_path=env_file_path, key_to_set="DESIGN_LINE3", value_to_set=data['design_line3'])
    set_key(dotenv_path=env_file_path, key_to_set="DESIGN_LINE4", value_to_set=data['design_line4'])
    set_key(dotenv_path=env_file_path, key_to_set="TITLE", value_to_set=data['title'])
    set_key(dotenv_path=env_file_path, key_to_set="TAGS", value_to_set=data['tags'])
    set_key(dotenv_path=env_file_path, key_to_set="SECTION", value_to_set=data['section'])

    return index()

@app.route('/generate-designs', methods=['POST','GET']) 
def generate_designs(): 
    
    current_design = [design_line1,design_line2,design_line3,design_line4]

    generateDesigns.MakeAllDesigns(current_design)

    return finished_gen_images()

@app.route('/generate-shirts', methods=['POST','GET']) 
def generate_shirts(): 
    
    designIndex = 0
    templateIndex = 0
    colorIndex = 0
    productType = 'shirts'


    generateMockups.generateAllImages(designIndex,templateIndex,colorIndex,productType)

    return finished_gen_images()

@app.route('/generate-sweatshirts', methods=['POST','GET']) 
def generate_sweatshirts(): 
    
    designIndex = 0
    templateIndex = 0
    colorIndex = 0
    productType = 'sweatshirts'


    generateMockups.generateAllImages(designIndex,templateIndex,colorIndex,productType)

    return finished_gen_images()

@app.route("/preview-images")
def preview_images():

    return render_template('images.html')

@app.route("/finished-gen-images")
def finished_gen_images():

    return render_template('finished_gen_images.html')

if __name__ == '__main__':
    app.run(debug=True, port=3003)