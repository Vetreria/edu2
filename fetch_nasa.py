import requests
import datetime
import dotenv
from file_save import save_image
import os.path


def get_nasa(nasa_token):
    links_img = []
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
            links_img.append(url)
    save_image(links_img, filename)


def get_epic(nasa_token):
    links_img = []
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
            links_img.append(url)
    save_image(links_img, filename)


def main():
    dotenv.load_dotenv()
    nasa_token = os.getenv('NASA_TOKEN')
    get_nasa(nasa_token)
    get_epic(nasa_token)


if __name__ == "__main__":
    main()
