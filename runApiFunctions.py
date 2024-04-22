import apiFunctions
import os
import json
from dotenv import load_dotenv
from datetime import timedelta,datetime


load_dotenv()

access=os.getenv('ACCESS_TOKEN')
refresh=os.getenv('REFRESH_TOKEN')
expire = datetime.utcnow() + timedelta(hours=1)
key=os.getenv('KEYSTRING')
productType = os.environ["PRODUCT_TYPE"]
SHOP_ID = os.getenv('SHOP_ID')

def fn_save(one, two, three):
    pass

# listingID = 1503513954

etsy = apiFunctions.EtsyAPI(key, access, refresh, expire, fn_save)

# data = etsy.get_listing_inventory(1490584318)
# json_object = json.dumps(data, indent=4)
# path = 'templates/products/old'+productType+'Listing.json'
# with open(path,'w') as outfile:
#     outfile.write(json_object)

for i in range(5,14):
    offset = 50 + (100 * i)

    data = etsy.get_listings_by_shop(SHOP_ID,limit=100,offset=offset)
    # json_object = json.dumps(data, indent=4)
    # path = 'templates/products/all'+productType+'Listings4212024.json'
    # with open(path,'w') as outfile:
    #     outfile.write(json_object)
    listings = data['results']
    for listing in listings:
        listingID = listing['listing_id']

        path = "templates/products/oldshirtsListing.json"

        shirtImagesList = [5916690381,5868605014,5063976754,5868605322]

        listingImages = etsy.get_listing_images(listingID)
        firstImage = listingImages['results'][0]['listing_image_id']

        print(firstImage)
        finalList = [firstImage]+shirtImagesList

        update = apiFunctions.UpdateListingRequest(
            image_ids=finalList
        )

        apiFunctions.updateListingInventory(etsy,listingID,path)

        etsy.update_listing(SHOP_ID,listingID,update)
