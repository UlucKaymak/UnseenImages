from functions.main import search_artworks, get_imageanddata, extractColor, prepare_tweet, post_tweet
import datetime
from termcolor import colored

   
print("")
print(colored(f"======== EXECUTE: {datetime.datetime.now()} ========", 'green'))

search_artworks()
get_imageanddata()
extractColor()
prepare_tweet()
post_tweet()
