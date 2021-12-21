from os import listdir
import os.path
from urllib.parse import urlparse
from pathlib import Path
import requests


def get_file_ext(url):
    cut = urlparse(url)
    return os.path.splitext(cut.path)[-1]


def save_image(url, filename):
    counter = 0
    file_ext = get_file_ext(url)
    while os.path.isfile(filename.format(counter, file_ext)):
        counter += 1
    file_ext = get_file_ext(url)
    filename = filename.format(counter, file_ext)
    os.path.split(filename)
    response = requests.get(url)
    response.raise_for_status()
    Path(os.path.split(filename)[0]).mkdir(parents=True, exist_ok=True)
    with open(filename, "wb") as file:
        file.write(response.content)