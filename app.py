
#Flask, os and env modules
import os
import time
from flask import Flask, render_template, request
from dotenv import set_key, load_dotenv
from pathlib import Path

#Custom Modules
import generateDesigns as generateDesigns
import generateMockups
import apiFunctions

#Etsy API Modules
from etsyv3.util.auth import AuthHelper

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
    productType=os.getenv('PRODUCT_TYPE')

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
                           productType=productType
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
    set_key(dotenv_path=env_file_path, key_to_set="PRODUCT_TYPE", value_to_set=data['productType'])


    os.environ["DESIGN_LINE1"] = data['design_line1']
    os.environ["DESIGN_LINE2"] = data['design_line2']
    os.environ["DESIGN_LINE3"] = data['design_line3']
    os.environ["DESIGN_LINE4"] = data['design_line4']
    os.environ["TITLE"] = data['title']
    os.environ["TAGS"] = data['tags']
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

    return finished()

@app.route("/preview-images")
def preview_images():

    return render_template('images.html')

@app.route("/finished")
def finished():

    return render_template('finished.html')

@app.route("/get-listing-inventory")
def get_listing_inventory():

    productType = "shirts"
    # etsy = apiFunctions.etsy
    
    designIndex = 0
    while designIndex < 6:
        # previousListing = etsy.get_listings_by_shop(apiFunctions.SHOP_ID,"draft")["results"][0]["listing_id"]
        # apiFunctions.generateListing()
        # time.sleep(3)
        # newListing = etsy.get_listings_by_shop(apiFunctions.SHOP_ID,"draft")["results"][0]["listing_id"]
        # while (previousListing == newListing):
        #     time.sleep(2)
        #     newListing = etsy.get_listings_by_shop(apiFunctions.SHOP_ID,"draft")["results"][0]["listing_id"]
        
        # listingID = newListing
        # print(listingID)

        # colorIndex = 0
        # pathToImage = "output/" + str(designIndex) + str(1) + ".jpg"
        # apiFunctions.uploadImages(listingID,pathToImage)
        # colorIndex +=1
        # for colorIndex in range(2,7):
        #     pathToImage = "output/" + str(designIndex) + str(colorIndex) + ".jpg"
        #     apiFunctions.uploadImages(listingID,pathToImage)
        #     colorIndex +=1

        # apiFunctions.updateListingInventory(productType,listingID)

        # apiFunctions.generateListing()
        # listingID = 3121241212
        # #Check for new listing and loop till a new one shows up
        # #Get new listing number
        
        # colorIndex = 0
        # pathToImage = "output/" + str(designIndex) + str(2) + ".jpg"
        # apiFunctions.uploadImages(listingID,pathToImage)
        # colorIndex +=1
        # for colorIndex in range(2,7):
        #     pathToImage = "output/" + str(designIndex) + str(colorIndex) + ".jpg"
        #     apiFunctions.uploadImages(listingID,pathToImage)
        #     colorIndex +=1

        # apiFunctions.updateListingInventory(productType,listingID)

        designIndex+=1


    return render_template("finished.html")

if __name__ == '__main__':
    app.run(debug=True, port=3003)