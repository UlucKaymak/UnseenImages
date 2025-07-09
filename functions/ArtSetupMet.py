from functions.path_var import current_data, data_classifications_file, data_queries_file, data_usedids_file
from termcolor import colored
import requests
import random
import json


# Store and read objectid's
def get_data_usedids():
    with open(data_usedids_file, "r") as file:
        return set(file.read().splitlines())
    return set()


def store_used_id(object_id):
    with open(data_usedids_file, "a") as file:
        file.write(f"{object_id}\n")


### Search artworks
def search_artworks():
    with open(data_queries_file, "r") as file:
        queries = [line.strip().replace(' ', '+') for line in file]

    query = random.choice(queries)

    print("")       
    print(colored("======== Search ========", 'light_cyan'))
    print(f"Arama Yapılan Query: {query}")

    search_url = "https://collectionapi.metmuseum.org/public/collection/v1/search?" + "&dateBegin=1100&hasImages=True&isPublicDomain=True&artistOrCulture=True" + f"&q={query}"
    response = requests.get(search_url)

    print(search_url)
    print("========")

    if response.status_code == 200:
        data_search = response.json()
            
        object_ids = data_search.get('objectIDs', [])
        if not object_ids:
            print(colored("Hiçbir sonuç bulunamadı.", 'red'))
            search_artworks()
            return

        data_usedids = get_data_usedids()
        available_ids = [id for id in object_ids if str(id) not in data_usedids]

        if not available_ids:
            print(colored("Tüm sonuçlar kullanılmış.", 'red'))
            return

        object_id = random.choice(available_ids)
        print(f"{len(object_ids)} sonuç bulundu.")

        store_artwork_details(object_id)
    else:
        print("Arama isteği başarısız oldu:", response.text)
        print("========")
        search_artworks() # Bir daha dene


### Get artwork details
def store_artwork_details(object_id):
    details_url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}"
    response = requests.get(details_url)

    if response.status_code == 200:
        data_artwork = response.json()

        image_url = data_artwork.get('primaryImage', None)
        page_url = data_artwork.get('objectURL', None)
        object_id = data_artwork["objectID"]
        previewdata_artist = data_artwork.get("artistDisplayName", "Unknown Artist")
        previewdata_title = data_artwork.get("title", "Untitled")
        previewdata_classification = data_artwork.get('classification', None)

        with open(data_classifications_file, "r") as file:
            allowed_classifications = [line.strip() for line in file]

        previewdata_classification = data_artwork.get('classification', None)
        if not previewdata_classification in allowed_classifications:
            print(colored(f"Sonuç uyumsuz classificationda. ({previewdata_classification})", 'red'))
            search_artworks()
        elif image_url:
            print("========")
            print(f"{object_id} seçildi.")
            print(f"Title: {previewdata_title}")
            print(f"Artist: {previewdata_artist}")
            print(f"Classification: {previewdata_classification}")
            print(f"Pre_image URL: {image_url}")
            print(f"Info URL: {page_url}")
            print("========")

            # Görsel alındığına göre bence artık data kaydedebilir.
            with open(current_data, "w") as file:
               json.dump(data_artwork, file)
            
            print("Yeni görsel için data kaydedildi.")
            store_used_id(object_id)
            print(colored("======== Search END ========", 'green'))

        else:
            print(colored(f"Bu sanat eserinin görseli mevcut değil. ID: {object_id}", 'red'))
            store_used_id(object_id=object_id)
            search_artworks() # Bir daha dene
    else:
        print(colored(f"Objenin detayları alınamadı. ID: {object_id}, Hata: {response.text}", 'red'))
        store_used_id(object_id=object_id)
        print("========")
        search_artworks() # Bir daha dene
