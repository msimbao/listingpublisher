
#Flask, os and env modules
import os
import json

from datetime import datetime, timedelta
from flask import Flask, render_template, request
from dotenv import set_key, load_dotenv
from pathlib import Path

#Custom Modules
import generateDesigns as generateDesigns
import generateMockups

#Etsy API Modules
from etsyv3.util.auth import AuthHelper
from etsyv3.enums import ListingRequestState, WhenMade, WhoMade
from etsyv3.models.file_request import UploadListingImageRequest
from etsyv3.models import UpdateListingRequest

from etsyv3 import EtsyAPI
from etsyv3.etsy_api import ETSY_API_BASEURL, Unauthorised
from etsyv3.models.listing_request import (
    CreateDraftListingRequest,
    UpdateListingInventoryRequest,
)

from etsyv3.models.product import Product

load_dotenv()

env_file_path = Path(".env")

#TODO add button for publish shirt images


#Define Variables for Current Design
name = 'Mphatso'


#Generate Authentication Link ALL REMAIN THE SAME
keystring=os.getenv('KEYSTRING')
state=os.getenv('STATE')
code_challenge=os.getenv('CODE_CHALLENGE')
auth_link = "https://www.etsy.com/oauth/connect?response_type=code&redirect_uri=http://localhost:3003/oauth/redirect&scope=email_r%20listings_r%20listings_w%20shops_r%20shops_w&client_id="+keystring+"&state="+state+"&code_challenge="+code_challenge+"&code_challenge_method=S256"

code_verifier = os.getenv('CODE_VERIFIER');
redirect_url=os.getenv('REDIRECT_URI')

app = Flask(__name__, static_folder='public', template_folder='views')

@app.route("/oauth/redirect")
def oauth_callback():
    state = request.args["state"]
    code = request.args["code"]
    auth = AuthHelper(
        keystring, redirect_url, code_verifier=code_verifier, state=state
    )
    auth.set_authorisation_code(code, state)
    token = auth.get_access_token()

    set_key(dotenv_path=env_file_path, key_to_set="ACCESS_TOKEN", value_to_set=token['access_token'])
    set_key(dotenv_path=env_file_path, key_to_set="REFRESH_TOKEN", value_to_set=token['refresh_token'])

    os.environ["ACCESS_TOKEN"] = token['access_token']
    os.environ["REFRESH_TOKEN"] = token['refresh_token']

    return finished()

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
                           tags=tags,
                           section=section
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

    os.environ["DESIGN_LINE1"] = data['design_line1']
    os.environ["DESIGN_LINE2"] = data['design_line2']
    os.environ["DESIGN_LINE3"] = data['design_line3']
    os.environ["DESIGN_LINE4"] = data['design_line4']
    os.environ["TITLE"] = data['title']
    os.environ["TAGS"] = data['tags']
    os.environ["SECTION"] = data['section']

    return finished()

@app.route('/generate-designs', methods=['POST','GET']) 
def generate_designs(): 
    
    current_design = [os.environ["DESIGN_LINE1"],os.environ["DESIGN_LINE2"],os.environ["DESIGN_LINE3"],os.environ["DESIGN_LINE4"]]

    generateDesigns.MakeAllDesigns(current_design)

    return finished()

@app.route('/generate-shirts', methods=['POST','GET']) 
def generate_shirts(): 
    
    designIndex = 0
    templateIndex = 0
    colorIndex = 0
    productType = 'shirts'

    generateMockups.generateAllImages(designIndex,templateIndex,colorIndex,productType)

    return finished()

@app.route('/generate-sweatshirts', methods=['POST','GET']) 
def generate_sweatshirts(): 
    
    designIndex = 0
    templateIndex = 0
    colorIndex = 0
    productType = 'sweatshirts'


    generateMockups.generateAllImages(designIndex,templateIndex,colorIndex,productType)

    return finished()

@app.route("/preview-images")
def preview_images():

    return render_template('images.html')

@app.route("/finished")
def finished():

    return render_template('finished.html')

@app.route("/get-listing-inventory")
def get_listing_inventory():

    def fn_save(one, two, three):
        pass

    EXPIRY_FUTURE = datetime.utcnow() + timedelta(hours=1)
    EXPIRY_PAST = datetime.utcnow() - timedelta(hours=1)

    KEYSTRING=os.getenv('KEYSTRING')
    ACCESS_TOKEN=os.getenv('ACCESS_TOKEN')
    REFRESH_TOKEN=os.getenv('REFRESH_TOKEN')

    etsy = EtsyAPI(KEYSTRING, ACCESS_TOKEN, REFRESH_TOKEN, EXPIRY_FUTURE, fn_save)
    etsy.get_authenticated_user()

    #Serialzing json
    data = etsy.get_listing_inventory(1692185454)
    json_object = json.dumps(data, indent=4)

    with open('output.json','w') as outfile:
        outfile.write(json_object)

    return render_template("finished.html")

if __name__ == '__main__':
    app.run(debug=True, port=3003)