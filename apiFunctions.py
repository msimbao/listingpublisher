 
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
import time

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
PRODUCT_TYPE=os.getenv('PRODUCT_TYPE')

def refreshEnvironmentVariableStores():
    global KEYSTRING,ACCESS_TOKEN,REFRESH_TOKEN,TAGS,TITLE,SHOP_ID,DESCRIPTION,PRODUCT_TYPE
    KEYSTRING=os.getenv('KEYSTRING')
    ACCESS_TOKEN=os.getenv('ACCESS_TOKEN')
    REFRESH_TOKEN=os.getenv('REFRESH_TOKEN')

    TAGS=os.getenv('TAGS')
    TITLE=os.getenv('TITLE')
    SHOP_ID=os.getenv('SHOP_ID')
    DESCRIPTION=os.getenv('DESCRIPTION')
    PRODUCT_TYPE=os.getenv('PRODUCT_TYPE')

etsy = EtsyAPI(KEYSTRING, ACCESS_TOKEN, REFRESH_TOKEN, EXPIRY_FUTURE, fn_save)

def saveMultipleListingsToJSON():
    data=etsy.get_listings_by_shop(SHOP_ID,ListingRequestState.DRAFT)
    json_object = json.dumps(data, indent=4)
    with open('output.json','w') as outfile:
        outfile.write(json_object)

def saveExampleListingToJSON(listingID,productType):
    data=etsy.get_listing(listingID)
    json_object = json.dumps(data, indent=4)
    path = 'templates/products/example'+productType+'Listing.json'
    with open(path,'w') as outfile:
        outfile.write(json_object)

def saveExampleListingImagesToJSON(listingID,productType):
    data=etsy.get_listing_images(listingID)
    json_object = json.dumps(data, indent=4)
    path = 'templates/products/example'+productType+'ImagesListing.json'
    with open(path,'w') as outfile:
        outfile.write(json_object)

def saveShopSectionsToJSON(listingID,productType):
    data=etsy.get_shop_sections(SHOP_ID)
    json_object = json.dumps(data, indent=4)
    with open('templates/products/sections.json','w') as outfile:
        outfile.write(json_object)


#Run to generate Info about the products
# saveExampleListingImagesToJSON(1710704203,'shirts')
# saveExampleListingToJSON(1710704203,'shirts')

# saveExampleListingImagesToJSON(1692185394,'sweatshirts')
# saveExampleListingToJSON(1692185394,'sweatshirts')


def generateListing(productType):
    #===============Create Draft Listing

    testimonailsID = [5868605322]
    otherImagesIDs = []
    shipping_profile_id = 0

    if productType == "shirts":
        shipping_profile_id=213749066457
        otherImagesIDs = [5916690381,5868605014,5868605450]
    else:
        shipping_profile_id=213746740947
        otherImagesIDs = [5916598883,5868757866,5868514582]

    image_ids = otherImagesIDs + testimonailsID

    listing = CreateDraftListingRequest(
            quantity=1,
            title=TITLE,
            description=DESCRIPTION,
            price=100,
            who_made=WhoMade.SOMEONE_ELSE,
            when_made=WhenMade.MADE_TO_ORDER,
            taxonomy_id=482,
            tags=TAGS.split(","),
            shipping_profile_id= shipping_profile_id,
            shop_section_id= 42395341,
            production_partner_ids=[2826409],
            image_ids=image_ids
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


def create_and_publish_baby():

    ACCESS_TOKEN=os.getenv('ACCESS_TOKEN')
    REFRESH_TOKEN=os.getenv('REFRESH_TOKEN')
    EXPIRY_FUTURE = datetime.utcnow() + timedelta(hours=1)
    etsy = EtsyAPI(KEYSTRING, ACCESS_TOKEN, REFRESH_TOKEN, EXPIRY_FUTURE, fn_save)

    productType =PRODUCT_TYPE
 
    designIndex=0

    while designIndex < 5:
        templateIndex = 0
        while templateIndex < 2:
            generateListing(productType)
            time.sleep(3)
            newListing = etsy.get_listings_by_shop(SHOP_ID,ListingRequestState.DRAFT)["results"][0]["listing_id"]

            listingID = newListing
            print(listingID)

            
            colorIndex = 0

            for colorIndex in range(2,7):
                pathToImage = "output/" + str(designIndex) + str(colorIndex) + ".jpg"
                uploadImages(listingID,pathToImage)
                time.sleep(3)
                colorIndex +=1

            pathToImage = "output/" + str(designIndex) + str(templateIndex) + ".jpg"
            uploadImages(listingID,pathToImage)

            updateListingInventory(productType,listingID)

            update = UpdateListingRequest(
                state=ListingRequestState.ACTIVE,
            )

            etsy.update_listing(SHOP_ID,listingID,update)
            templateIndex+=1
        designIndex+=1
