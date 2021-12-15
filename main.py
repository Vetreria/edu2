import telegram
import requests
from pathlib import Path
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


def nasa_image(nasa_token):
    response = requests.get(
        f"https://api.nasa.gov/planetary/apod/", params={
            "api_key": nasa_token, "count": 50
            }
    )
    response.raise_for_status()
    filename = "nasa/nasa{}{}"
    for link in response.json():
        url = link.get("hdurl")
        if url is not None:
            save_image(url, filename)


def requst_epic(nasa_token):
    filename = "epic/epic{}{}"
    response = requests.get(
        "https://api.nasa.gov/EPIC/api/natural/", params={"api_key": nasa_token}
    )
    response.raise_for_status()
    for param in response.json():
        name = param.get("image")
        d_str = param.get("date")
        d_img = datetime.datetime.strptime(d_str, "%Y-%m-%d %H:%M:%S")
        if name or d_image is not None:
            # year = d_image.year
            url = (
                """https://epic.gsfc.nasa.gov/archive/natural/{}/{}/{}/png/{}.png"""
                .format(d_img.year, d_img.month, d_img.day, name)
            )
            save_image(url, filename)


def bot_send_text(bot):
    bot.send_message(chat_id='@antonspacetest', text="I'm sorry Dave I'm afraid I can't do that.")


def bot_send_photo(bot):
    bot.send_photo(chat_id='@antonspacetest', photo=open('nasa/nasa10.jpg', 'rb'))


def main():
    dotenv.load_dotenv()
    tg_token = os.getenv('TG_TOKEN')
    bot = telegram.Bot(token = tg_token)
    nasa_token = os.getenv('NASA_TOKEN')
    # spasex()
    # nasa_image(nasa_token)
    # requst_epic(nasa_token)
    print(bot.get_me())
    bot_send_photo(bot)


if __name__ == "__main__":
    main()
