from functions.path_var import current_data, palette_output_folder
from termcolor import colored
import tweepy
import json

API_KEY = '-'
API_SECRET_KEY = '-'
BEARER_TOKEN = '-'
ACCESS_TOKEN = '-'
ACCESS_TOKEN_SECRET = '-'

# Initialize Tweepy v2
client = tweepy.Client(consumer_key=API_KEY,    
                    consumer_secret=API_SECRET_KEY,
                    access_token=ACCESS_TOKEN,
                    access_token_secret=ACCESS_TOKEN_SECRET)
    
# Initialize Tweepy v1.1
auth = tweepy.OAuth1UserHandler(consumer_key=API_KEY, 
                                consumer_secret=API_SECRET_KEY, 
                                access_token=ACCESS_TOKEN, 
                                access_token_secret=ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

def post_tweet():
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
        media = api.media_upload(postdata_image)

        # Tweepy v2 Client
        response = client.create_tweet(text=tweet_text, media_ids=[media.media_id])
        tweet_url = f"https://twitter.com/{ACCESS_TOKEN.split('-')[0]}/status/{response.data['id']}"
        print(colored("Tweet successfully posted!", "green"))
        print(f"Tweet URL: {tweet_url}")
        print(colored("======== POSTING END ========", 'green'))
    except tweepy.TweepyException as e:
        print(colored(f"Tweet posting failed: {e}", "red"))
        print(f"Error details: {e.args}")
