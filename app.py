

import os
from flask import Flask, render_template
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
#switch everything to .env file-
#switch designs to input form edit system
#add button for generate designs
#add buttons for generate shirt images
#add button for preview shirt images
#add button for publish shirt images
#do all this for sweatshirts too

#Define Variables for Current Design
animal = 'Mphatso'
design_line1=os.getenv('DESIGN_LINE1')
design_line2=os.getenv('DESIGN_LINE2')
design_line3=os.getenv('DESIGN_LINE3')
design_line4=os.getenv('DESIGN_LINE4')

#Generate Authentication Link
client_id=os.getenv('KEYSTRING')
state=os.getenv('STATE')
code_challenge=os.getenv('CODE_CHALLENGE')
auth_link = "https://www.etsy.com/oauth/connect?response_type=code&redirect_uri=http://localhost:3003/oauth/redirect&scope=email_r%20listings_r%20listings_w%20shops_r%20shops_w&client_id="+client_id+"&state="+state+"&code_challenge="+code_challenge+"&code_challenge_method=S256"

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html',
                           value=animal,
                           auth_link=auth_link,
                           design_line1=design_line1,
                           design_line2=design_line2,
                           design_line3=design_line3,
                           design_line4=design_line4
                           )


