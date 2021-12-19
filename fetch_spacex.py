import requests
from pathlib import Path
from os import listdir
import os.path
from urllib.parse import urlparse
import dotenv


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


def get_lunch():
    response = requests.get("https://api.spacexdata.com/v3/launches/27")
    response.raise_for_status()
    lunch = response.json()
    dict_links = lunch.get("links")
    links_list = dict_links.get("flickr_images")
    return links_list


def spasex():
    filename = "images/spacex{}{}"
    for url in get_lunch():
        save_image(url, filename)


def main():
    dotenv.load_dotenv()
    tg_token = os.getenv('TG_TOKEN') 
    spasex()


if __name__ == "__main__":
    main()
