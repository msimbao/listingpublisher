 
from datetime import datetime, timedelta
import json
import os
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
from math import pi

from pathlib import Path
from dotenv import load_dotenv

def fn_save(one, two, three):
    pass

env_path = Path('.', '.env')
load_dotenv(dotenv_path=env_path)

EXPIRY_FUTURE = datetime.utcnow() + timedelta(hours=1)
EXPIRY_PAST = datetime.utcnow() - timedelta(hours=1)

KEYSTRING=os.getenv('KEYSTRING')
ACCESS_TOKEN=os.getenv('ACCESS_TOKEN')
REFRESH_TOKEN=os.getenv('REFRESH_TOKEN')

TAGS=os.getenv('TAGS')
TITLE=os.getenv('TITLE')
SHOP_ID=os.getenv('SHOP_ID')
DESCRIPTION=os.getenv('DESCRIPTION')

etsy = EtsyAPI(KEYSTRING, ACCESS_TOKEN, REFRESH_TOKEN, EXPIRY_FUTURE, fn_save)

def saveMultipleListingsToJSON():
    data=etsy.get_listings_by_shop(SHOP_ID,ListingRequestState.DRAFT)
    json_object = json.dumps(data, indent=4)
    with open('output.json','w') as outfile:
        outfile.write(json_object)

def saveExampleListingToJSON():
    data=etsy.get_listing(1710704203)
    json_object = json.dumps(data, indent=4)
    with open('exampleListing.json','w') as outfile:
        outfile.write(json_object)

def saveExampleListingImagesToJSON():
    data=etsy.get_listing_images(1710704203)
    json_object = json.dumps(data, indent=4)
    with open('exampleListingImages.json','w') as outfile:
        outfile.write(json_object)


def generateListing():
    #===============Create Draft Listing
    listing = CreateDraftListingRequest(
            quantity=1,
            title=TITLE,
            description=DESCRIPTION,
            price=100,
            who_made=WhoMade.SOMEONE_ELSE,
            when_made=WhenMade.MADE_TO_ORDER,
            taxonomy_id=482,
            tags=TAGS.split(","),
            shipping_profile_id= 213749066457,
            shop_section_id= 42393967,
            production_partner_ids=[2826409],
            image_ids=[5868605322,5916690381,5868605014,5868605450]
        )
    
    etsy.create_draft_listing(SHOP_ID,listing)

def uploadImages(listingID,pathToImage):
    listing_image_upload = UploadListingImageRequest(
            image_bytes=UploadListingImageRequest.generate_bytes_from_file(
                pathToImage
            )
        )
    etsy.upload_listing_image(SHOP_ID,listingID,listing_image_upload)

def getListingInventory(listingID):
    data = etsy.get_listing_inventory(listingID)
    json_object = json.dumps(data, indent=4)

    with open('output.json','w') as outfile:
        outfile.write(json_object)

def updateListingInventory(productType,listingID):
    product_list = []
    # Opening JSON file
    path = 'templates/products/' + productType + ".json"
    with open(path) as json_file:
        data = json.load(json_file)

        products = data['products']
        offerings = []
        properties = []

        for product in products:
            offerings = product['offerings']
            del offerings[0]['is_deleted']
            del offerings[0]['offering_id']
            offerings[0]['is_enabled'] = True

            price = '{0:.2f}'.format(offerings[0]['price']['amount'] / offerings[0]['price']['divisor'])
            offerings[0]['price'] = price

            properties = product['property_values']
            for property in properties:
                del property['scale_id']
                del property['scale_name']

            productToWrite = Product("",properties,offerings)
            product_list.append(productToWrite)

    price_on_property = [513,514]
    quantity_on_property = [513,514]

    listing_inventory_request = UpdateListingInventoryRequest(product_list, price_on_property, quantity_on_property, 0)

    etsy.update_listing_inventory(listingID,listing_inventory_request)


import time

# listing = CreateDraftListingRequest(
#         quantity=1,
#         title=TITLE,
#         description=DESCRIPTION,
#         price=100,
#         who_made=WhoMade.SOMEONE_ELSE,
#         when_made=WhenMade.MADE_TO_ORDER,
#         taxonomy_id=482,
#         tags=TAGS.split(","),
#         shipping_profile_id= 213749066457,
#         shop_section_id= 42393967,
#         production_partner_ids=[2826409]
#     )

# etsy.create_draft_listing(SHOP_ID,listing)

generateListing()
time.sleep(3)
newListing = etsy.get_listings_by_shop(SHOP_ID,ListingRequestState.DRAFT)["results"][0]["listing_id"]

listingID = newListing
print(listingID)
productType ='shirts'

designIndex=0
colorIndex = 0

for colorIndex in range(2,7):
    pathToImage = "output/" + str(designIndex) + str(colorIndex) + ".jpg"
    uploadImages(listingID,pathToImage)
    colorIndex +=1

pathToImage = "output/" + str(designIndex) + str(1) + ".jpg"
uploadImages(listingID,pathToImage)

updateListingInventory(productType,listingID)
