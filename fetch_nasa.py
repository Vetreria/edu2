import requests
from pathlib import Path
from os import listdir
import os.path
from urllib.parse import urlparse
import datetime
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


def nasa_image(nasa_token):
    response = requests.get(
        f"https://api.nasa.gov/planetary/apod/", params={
            "api_key": nasa_token, "count": 50
            }
    )
    response.raise_for_status()
    filename = "images/nasa{}{}"
    for link in response.json():
        url = link.get("hdurl")
        if url is not None:
            save_image(url, filename)


def requst_epic(nasa_token):
    filename = "images/epic{}{}"
    response = requests.get(
        "https://api.nasa.gov/EPIC/api/natural/", params={"api_key": nasa_token}
    )
    response.raise_for_status()
    for param in response.json():
        name = param.get("image")
        d_str = param.get("date")
        d_img = datetime.datetime.strptime(d_str, "%Y-%m-%d %H:%M:%S")
        if name or d_img is not None:
            url = (
                """https://epic.gsfc.nasa.gov/archive/natural/{}/{}/{}/png/{}.png"""
                .format(d_img.year, d_img.month, d_img.day, name)
            )
            save_image(url, filename)


def main():
    dotenv.load_dotenv()
    nasa_token = os.getenv('NASA_TOKEN')
    nasa_image(nasa_token)
    requst_epic(nasa_token)


if __name__ == "__main__":
    main()
