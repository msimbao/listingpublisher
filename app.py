

import os
from flask import Flask, render_template, request
from dotenv import set_key, load_dotenv
from pathlib import Path

load_dotenv()

# env_file_path = Path(".env")
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

#Define Variables for Current Design
name = 'Mphatso'
design_line1=os.getenv('DESIGN_LINE1')
design_line2=os.getenv('DESIGN_LINE2')
design_line3=os.getenv('DESIGN_LINE3')
design_line4=os.getenv('DESIGN_LINE4')

title=os.getenv('TITLE')
tags=os.getenv('TAGS')
section=os.getenv('SECTION')

#Generate Authentication Link
client_id=os.getenv('KEYSTRING')
state=os.getenv('STATE')
code_challenge=os.getenv('CODE_CHALLENGE')
auth_link = "https://www.etsy.com/oauth/connect?response_type=code&redirect_uri=http://localhost:3003/oauth/redirect&scope=email_r%20listings_r%20listings_w%20shops_r%20shops_w&client_id="+client_id+"&state="+state+"&code_challenge="+code_challenge+"&code_challenge_method=S256"

app = Flask(__name__, static_folder='public', template_folder='views')

@app.route("/")
def index():
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
    return { 
        'design_line1'     : data['design_line1'], 
        'design_line2'     : data['design_line2'],
        'design_line3'     : data['design_line3'], 
        'design_line4'     : data['design_line4'], 
        'title'     : data['title'], 
        'tags'     : data['tags'], 
        'section'     : data['section'],         

        # 'gender'      : 'Male' if data['genderMale'] else 'Female', 
    } 


