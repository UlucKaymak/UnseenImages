import requests
import json
import random
import os

current_data = "processing_folder/data/current_data.json"
data_usedids_file = "processing_folder/data/data_usedids.txt"
data_queries_file = "processing_folder/data/data_queries.txt"

# Kullanılmış ID'leri oku
def get_data_usedids():
    if os.path.exists(data_usedids_file):
        with open(data_usedids_file, "r") as file:
            return set(file.read().splitlines())
    return set()

# Kullanılmış ID'leri kaydet
def store_used_id(object_id):
    with open(data_usedids_file, "a") as file:
        file.write(f"{object_id}\n")

# Arama fonksiyonu
def search_paintings():

    with open(data_queries_file, "r") as file:
        queries = [line.strip().replace(' ', '+') for line in file]

    query = random.choice(queries)
    print(query)

    url = f"https://www.wikiart.org/en/api/2/PaintingSearch?term={query}"
    print(url)
    print("Bağlanılıyor...")

    try:
        response = requests.get(url)

        if response.status_code == 200:
            exported_data = response.json()
            print("Bağlanıldı.")

            # JSON verisini dosyaya kaydet
            with open(current_data, "w") as file:
                json.dump(exported_data, file)

            if exported_data["data"]:
                data_usedids = get_data_usedids()
                available_paintings = [painting for painting in exported_data["data"] if painting["id"] not in data_usedids]
                return available_paintings
            else:
                print("Sonuç bulunamadı.")
                return []
        else:
            print(f"API isteği başarısız oldu, hata kodu: {response.status_code}")
            print(f"Cevap: {response.text}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Bir hata oluştu: {e}")
        return []

# Store fonksiyonu
def store_painting():

    with open(current_data, "r") as file:
        data_artwork = json.load(file)

    if not data_artwork:
        print("Kullanılacak eser yok.")
        return
    
    object_id = data_artwork.get("id")
    image_url = data_artwork.get("image_url")
    artist_name = data_artwork.get("artist_name")
    painting_title = data_artwork.get("painting_title")

    print("========")
    print(object_id)
    print(image_url)
    print(artist_name)
    print(painting_title)
    print("========")

    # Görseli indir ve kaydet
    image_response = requests.get(image_url, stream=True)
    if image_response.status_code == 200:
        image_path = os.path.join('test_data', f'pre_image{object_id}.jpg')
        with open(image_path, 'wb') as file:
            for chunk in image_response.iter_content(1024):
                file.write(chunk)
        print("Görsel başarıyla kaydedildi!")

        # Eserin bilgilerini JSON dosyasına kaydet
        painting_info = {
            "artist_name": artist_name,
            "painting_title": painting_title,
            "image_url": image_url,
            "id": object_id  # ID'yi de kaydet
        }

        json_path = os.path.join('test_data', 'painting_info.json')
        with open(json_path, 'w') as json_file:
            json.dump(painting_info, json_file, indent=4)

        # ID'yi kullanılmışlar listesine kaydet
        store_used_id(object_id)
        print(f"Eser bilgileri ve ID kaydedildi: {object_id}")
    else:
        print(f"Görsel indirilemedi, hata kodu: {image_response.status_code}")

search_paintings()
store_painting()