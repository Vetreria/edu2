from pathlib import Path
import requests
import datetime
import dotenv
from file_save import save_images
import os.path


def get_nasa(nasa_token):
    image_links = []
    response = requests.get(
        "https://api.nasa.gov/planetary/apod/", params={
            "api_key": nasa_token, "count": 50
            }
    )
    response.raise_for_status()
    print(response.json)
    filename = "images/nasa{}{}"
    for link in response.json():
    
        url = link.get("hdurl")
        if url:
            image_links.append(url)
    save_images(image_links, filename)



def get_epic(nasa_token):
    image_links = []
    filename = "images/epic{}{}"
    response = requests.get(
        "http://api.nasa.gov/EPIC/api/natural/", params={"api_key": nasa_token}
    )
    response.raise_for_status()
    print(response.json())
    for param in response.json():
        name = param.get("image")
        # date_value = param.get("date")
        date_value = datetime.datetime.strptime(param.get("date"), "%Y-%m-%d %H:%M:%S")
        if name or date_value:
            url = (
                "https://epic.gsfc.nasa.gov/archive/natural/{}/{}/{}/png/{}.png"
                .format(date_value.year, date_value.month, date_value.day, name)
            )
            image_links.append(url)
    save_images(image_links, filename)
    


def main():
    Path("images").mkdir(parents=True, exist_ok=True)
    dotenv.load_dotenv()
    nasa_token = os.getenv('NASA_TOKEN')
    get_nasa(nasa_token)
    # get_epic(nasa_token)


if __name__ == "__main__":
    main()
