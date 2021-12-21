import requests
from file_save import save_image


def get_launch():
    response = requests.get("https://api.spacexdata.com/v3/launches/27")
    response.raise_for_status()
    launch = response.json()
    launch_links = launch.get("links")
    links_img = launch_links.get("flickr_images")
    return links_img


def save_spasex():
    filename = "images/spacex{}{}"
    for url in get_launch():
        save_image(url, filename)


def main():
    save_spasex()


if __name__ == "__main__":
    main()
