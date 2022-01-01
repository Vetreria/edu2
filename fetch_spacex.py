import requests
from file_save import save_image


def get_launch():
    response = requests.get("https://api.spacexdata.com/v3/launches/27")
    response.raise_for_status()
    links_img = response.json()['links']['flickr_images']
    filename = "images/spacex{}{}"
    save_image(links_img, filename)


def main():
    get_launch()


if __name__ == "__main__":
    main()
