from functions.path_var import current_data, palette_output_folder
from termcolor import colored
import tweepy
import json

API_KEY = 'bJmDaKCfQRRpH9lTFLumA1ObK'
API_SECRET_KEY = 'ubt4pMXMUiB9w3eyCcf30Tusqvg9qBYJC7s1JZaYsF0ZtL7clT'
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAC%2F8vQEAAAAArk%2BALPRsYcKSzU6bEBqUav6HQag%3DpqVWH7fDph5KGT08ZKQsTXOeRkiHDhjkNWv7OS2zXKFHdPHSCh'
ACCESS_TOKEN = '1826593040430940161-nml90CwWrVCFaMwkxvKL5ltYr5pFb0'
ACCESS_TOKEN_SECRET = 'qdeHvAZ5IBCkLPuVsw6qaBqGocIy4yKY5c748YB5cFFUG'

    # Initialize Tweepy v2 Client for creating the tweet
client = tweepy.Client(consumer_key=API_KEY,    
                    consumer_secret=API_SECRET_KEY,
                    access_token=ACCESS_TOKEN,
                    access_token_secret=ACCESS_TOKEN_SECRET)
    
    # Initialize Tweepy v1.1 API for media upload
auth = tweepy.OAuth1UserHandler(consumer_key=API_KEY, 
                                consumer_secret=API_SECRET_KEY, 
                                access_token=ACCESS_TOKEN, 
                                access_token_secret=ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

def post_tweet():
    # Read data from current_data.json file
    with open(current_data, "r") as file:
        data_artwork = json.load(file)

    postdata_title = data_artwork.get('title', "Untitled")
    postdata_artist = data_artwork.get('artistDisplayName', "Unknown Artist")
    object_id = data_artwork.get('objectID')
    postdata_image = palette_output_folder + f"{object_id}.jpg"

    tweet_text = f'"{postdata_title}"\n{postdata_artist}'

    # print(postdata_image)
    # print(tweet_text)

    try:
        # Upload image using Tweepy v1.1 API
        media = api.media_upload(postdata_image)

        # Create the tweet with media attached using Tweepy v2 Client
        response = client.create_tweet(text=tweet_text, media_ids=[media.media_id])
        tweet_url = f"https://twitter.com/{ACCESS_TOKEN.split('-')[0]}/status/{response.data['id']}"
        print(colored("Tweet successfully posted!", "green"))
        print(f"Tweet URL: {tweet_url}")
        print(colored("======== POSTING END ========", 'green'))
    except tweepy.TweepyException as e:
        print(colored(f"Tweet posting failed: {e}", "red"))
        print(f"Error details: {e.args}")