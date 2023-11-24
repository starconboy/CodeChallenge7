import ascii_magic
import requests
import json
import io
from PIL import Image
from boombox import BoomBox

# Functional requirements
#  1 - generate ascii art from a real image of a duck
#  2 - Random Duck API: https://random-d.uk/api
#  3 - Width and height of the ascii art should be <= 80
#  4 - (optional) Extra credit: add audio


def simple_network_request(url: str) -> requests.Response:
        failed = "FAILED"
        response = None
        try:
            response = requests.get(url, timeout=30)
        except Exception as e:
            return failed
        try:
            if response.status_code != 200:
                return failed
        except Exception as e:
            return failed
        # return the network response
        return response

def get_image(url: str) -> Image:
     raw_image = simple_network_request(url)     
     img_byte_arr = io.BytesIO(raw_image.content)
     return Image.open(img_byte_arr)

def resize_image(image: Image) -> Image:
     width = image.width
     height = image.height
     ratio = 1
     if width >= height:
          ratio = width / 80
     else:
          ratio = height / 80
     if ratio > 1:
          (w, h) = ((int)(width // ratio), (int)(height // ratio))
          image = image.resize((w, h))
     
     return image


# Functional requirement 2
random_duck = simple_network_request('https://random-d.uk/api/random')
print(random_duck)
if random_duck != "FAILED":
    random_duck_json = json.loads(random_duck.text)
    image_url = random_duck_json['url']
    image = get_image(image_url)

    # Functional requirement 3, part 1 (you need to resize the image otherwise the ascii art when requested to do 80 columns cuts part of the image off)
    image = resize_image(image)
    output = ascii_magic.from_pillow_image(image)

    # Functional requirement 4
    boombox = BoomBox('quack-quack.wav').play()
    # Functional requirement 3, part 2 (ascii art outputs higher than 80 columns unless a number is specified even if the image is only 80 pixels) 
    # Functional requirement 1
    output.to_terminal(columns=80)
    # Functional requirement 4: this is needed for consistent audio playback, boombox stops playback if the script ends
    input("press {enter} to exit")
    