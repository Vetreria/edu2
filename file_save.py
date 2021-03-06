import os.path
import os
from urllib.parse import urlparse
import requests


def get_file_ext(url):
    cut = urlparse(url)
    return os.path.splitext(cut.path)[-1]


def save_images(image_links, filename):
    for number, link in enumerate(image_links, 1):
        response = requests.get(link)
        response.raise_for_status()
        file_ext = get_file_ext(link)
        with open(filename.format(number, file_ext), "wb") as file:
            file.write(response.content)

