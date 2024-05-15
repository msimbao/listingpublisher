
#Flask, os and env modules
import os
import time
from flask import Flask, render_template, request
from dotenv import set_key, load_dotenv
from pathlib import Path
import webbrowser
from datetime import datetime, timedelta

#Custom Modules
import generateDesigns as generateDesigns
import generateMockups
import apiFunctions

#Etsy API Modules
from etsyv3 import EtsyAPI
from etsyv3.util.auth import AuthHelper

load_dotenv()

env_file_path = Path(".env")

#TODO add button for publish shirt images

#Define Variables for Current Design
name = 'Mphatso'

sections_dictionary = {
    42378910 : "Book Lover",
    42393967 : "Food",
    42395337 : "Funny Other",
    42395341 : "Hobby / Passion / Other",
    42395343 : "Sport",
    42395347 : "Farm Life / Country",
    42395351 : "Introvert",
    42381728 : "Conditions",
    42395359 : "Camping / Lake / Travel",
    42381732 : "Nurse / Dentist / Doctor",
    42381736 : "Real Estate",
    42381740 : "Flower / Plant Lover",
    42381742 : "Dog / Cat / Animal",
    42381746 : "Baking / Cookie Lover",
    42381752 : "Teacher / Therapist",
    42381754 : "Inspirational",
    42381756 : "Pregnancy Announcement",
    42381760 : "Wedding Bridal Party",
    42395385 : "Mom, Dad, Family"
}

#Generate Authentication Link ALL REMAIN THE SAME
keystring=os.getenv('KEYSTRING')
state=os.getenv('STATE')
code_challenge=os.getenv('CODE_CHALLENGE')
auth_link = "https://www.etsy.com/oauth/connect?response_type=code&redirect_uri=http://localhost:3003/oauth/redirect&scope=email_r%20listings_r%20listings_w%20shops_r%20shops_w&client_id="+keystring+"&state="+state+"&code_challenge="+code_challenge+"&code_challenge_method=S256"

code_verifier = os.getenv('CODE_VERIFIER');
redirect_url=os.getenv('REDIRECT_URI')

def fn_save(one, two, three):
    pass

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
    productType=os.getenv('PRODUCT_TYPE')
    section_name = sections_dictionary[int(section)]
    

    return render_template('index.html',
                           name=name,
                           auth_link=auth_link,
                           design_line1=design_line1,
                           design_line2=design_line2,
                           design_line3=design_line3,
                           design_line4=design_line4,
                           title=title,
                           tags=tags,
                           section=section,
                           productType=productType,
                           section_name = section_name
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
    set_key(dotenv_path=env_file_path, key_to_set="TAGS", value_to_set=data['tags'].replace('"', ''))
    set_key(dotenv_path=env_file_path, key_to_set="SECTION", value_to_set=data['section'])
    set_key(dotenv_path=env_file_path, key_to_set="PRODUCT_TYPE", value_to_set=data['productType'])


    os.environ["DESIGN_LINE1"] = data['design_line1']
    os.environ["DESIGN_LINE2"] = data['design_line2']
    os.environ["DESIGN_LINE3"] = data['design_line3']
    os.environ["DESIGN_LINE4"] = data['design_line4']
    os.environ["TITLE"] = data['title']
    os.environ["TAGS"] = data['tags'].replace('"', '')
    os.environ["SECTION"] = data['section']
    os.environ["PRODUCT_TYPE"] = data['productType']

    return finished()

@app.route('/generate-designs', methods=['POST','GET']) 
def generate_designs(): 
    
    current_design = [os.environ["DESIGN_LINE1"],os.environ["DESIGN_LINE2"],os.environ["DESIGN_LINE3"],os.environ["DESIGN_LINE4"]]

    generateDesigns.MakeAllDesigns(current_design)

    return finished()

@app.route('/generate-mockups', methods=['POST','GET']) 
def generate_mockups(): 
    
    designIndex = 0
    templateIndex = 0
    colorIndex = 0
    productType = os.environ["PRODUCT_TYPE"]

    generateMockups.generateAllImages(designIndex,templateIndex,colorIndex,productType)

    return preview_images()

@app.route("/preview-images")
def preview_images():

    return render_template('images.html')

@app.route("/finished")
def finished():

    return render_template('finished.html')

@app.route("/get-listing-inventory")
def get_listing_inventory():

    load_dotenv()

    access=os.getenv('ACCESS_TOKEN')
    refresh=os.getenv('REFRESH_TOKEN')
    expire = datetime.utcnow() + timedelta(hours=1)
    key=os.getenv('KEYSTRING')
    productType = os.environ["PRODUCT_TYPE"]

    etsy = EtsyAPI(key, access, refresh, expire, fn_save)

    # apiFunctions.refreshEnvironmentVariableStores()
    apiFunctions.create_and_publish_baby(etsy,productType)

    return render_template("finished.html")

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:3003/')  # Go to example.com
    app.run(port=3003)
