from pathlib import Path
import requests
from file_save import save_image, save_images


def get_launch():
    response = requests.get("https://api.spacexdata.com/v3/launches/27")
    response.raise_for_status()
    image_links = response.json()['links']['flickr_images']
    filename = "images/spacex{}{}"
    save_images(image_links, filename)


def main():
    Path("images").mkdir(parents=True, exist_ok=True)
    get_launch()


if __name__ == "__main__":
    main()
