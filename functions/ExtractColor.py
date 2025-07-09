from functions.path_var import current_data, input_preimage_folder, resized_image_folder, palette_output_folder
from termcolor import colored
from PIL import Image, ImageDraw, ImageFilter
from colorthief import ColorThief
import os
import json

#Variables
num_colors = 7
aspect_ratio = 2 / 1
palette_height = 300


def get_image_data():
    with open(current_data, "r") as file:
        data_artwork = json.load(file)

    object_id = data_artwork['objectID']
    print("")
    print(colored("======== Color Extraction ========", 'light_yellow'))

    preimage_path = input_preimage_folder + f"{object_id}" + ".jpg"
    resize_image(preimage_path, object_id=object_id)    

# Function to resize image for color processing
def resize_image(input_path, object_id, size=(250, 250)):
    print(f"ORJImage: {input_path}")
    resized_output_path = resized_image_folder +f"{object_id}" +".jpg"

    try:
        with Image.open(input_path) as img:
            img.thumbnail(size)
            img.save(resized_output_path)
            print(f"Küçültülmüş görsel kaydedildi: {resized_output_path}")
            print("========")
    except Exception as e:
        print(colored(f"Error resizing image: {e}", 'red'))

    get_color_palette(resized_output_path, object_id=object_id)

# Function to extract color palette from an image
def get_color_palette(resized_image_path, object_id):
    try:
        color_thief = ColorThief(resized_image_path)
        palette = color_thief.get_palette(color_count=num_colors)
        print(f"Renk paleti çıkartıldı.")
        print("========")
    except Exception as e:
        print(f"Error extracting color palette: {e}")

    create_palette_image(palette, object_id)



# Function to create and save a color palette image
def create_palette_image(palette, object_id):

    # 3:4 aspect ratio için palet boyutları
    palette_width = int(palette_height * aspect_ratio)

    # Her renk bloğunun genişliği, paletin toplam genişliğine tam uyacak şekilde ayarlanır
    block_width = palette_width // len(palette)

    # Beyaz çerçeveli bir görsel oluştur
    frame_width = 20  # Çerçevenin genişliği
    total_width = palette_width + 2 * frame_width
    total_height = palette_height + 2 * frame_width
    palette_img = Image.new("RGB", (total_width, total_height), "white")
    draw = ImageDraw.Draw(palette_img)

    # Çerçeve görselinin içine renk paletini ekle
    palette_image = Image.new("RGB", (palette_width, palette_height), "white")
    draw_palette = ImageDraw.Draw(palette_image)

    for i, color in enumerate(palette):
        draw_palette.rectangle(
            [i * block_width, 0, (i + 1) * block_width, palette_height],
            fill=color
        )

    # Renk paletini çerçevenin içine yerleştir
    palette_img.paste(palette_image, (frame_width, frame_width))

    file_name = palette_output_folder + f"{object_id}" + ".jpg"
    palette_img.save(file_name, optimize=True)
    print(f"Renk paleti görseli '{file_name}' olarak kaydedildi.")
    print('========')
    print(colored("======== Color Extraction END ========", 'green'))
