from functions.path_var import current_data, input_preimage_folder
import json
import requests
import tweepy
from termcolor import colored
from functions.ArtSetupMet import search_artworks, current_data
from functions.ExtractColor import get_image_data
from functions.TwitterAPI import post_tweet, API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET


def get_imageanddata():

    with open(current_data, "r") as file:
        data_artwork = json.load(file)
    
    object_id = data_artwork["objectID"]
    title = data_artwork.get('title', "Unknown Name")
    artist = data_artwork.get('artistDisplayName', "Unknown Artist")
    classification = data_artwork["classification"]
    imageURL = data_artwork["primaryImage"]

    print("")
    print(colored("======== Save PreImage ========", 'light_magenta'))
    print(f"ObjectID: {object_id}")
    print(f"Title: {title}")
    print(f"Artist: {artist}")
    print(f"Classification: {classification}")
    print("========")
    print(f"URL: {imageURL}")

    response = requests.get(imageURL)
    preimagefilename = input_preimage_folder + f"{object_id}.jpg"
    preimagefilenamepreview = f"pre_image{object_id}.jpg"
    if response.status_code == 200:
        with open(preimagefilename, "wb") as file:
            file.write(response.content)  # Write the image content to the file
        print(f"Preimage kaydedildi. '{preimagefilenamepreview}'")
        print("========")

        print(colored("======== Save PreImage END========", 'green')) 
    else:
        print(colored(f"Görsel kaydedilemedi. Status code: {response.status_code}", 'red'))
        print("========")
        errorfix_404()

def errorfix_404():
    search_artworks() # Yeni görsel aramaya başlar
    get_imageanddata()

def extractColor():
    get_image_data()

def create_api():
    """API'yi oluşturmak için kimlik doğrulaması yapar."""
    auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    return api

def prepare_tweet():
    """Tweet içeriğini ve görseli hazırlar."""
    with open(current_data, "r") as file:
        data_artwork = json.load(file)
    
    postdata_title = data_artwork.get('title', "Untitled")
    postdata_artist = data_artwork.get('artistDisplayName', "Unknown Artist")
    object_id = data_artwork.get('objectID')
    postdata_image = f"processing_folder/paletteoutput/palette_output{object_id}.jpg"

    print("")
    print(colored("======== Prepare Tweet ========", 'light_blue'))
    print(postdata_image)
    tweet_text = f'"{postdata_title}"\n{postdata_artist}'
    print(tweet_text)
    print("========")
    
    return tweet_text, postdata_image
