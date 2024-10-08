import time
import random
import os
import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import re
from string import ascii_lowercase
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pathlib

def save_file(
        path,
        text,
        replace=False
):
    if not replace:

        if os.path.exists(os.path.relpath(path + ".txt")):
            path = pathlib.PurePath(path)
            base_path = path.parent
            songname = path.stem
            songname = re.sub('[^A-Za-z0-9]+', '', songname)
            finalpath = os.path.join(base_path, songname)

            file = open(finalpath + "_2" + ".txt", "w")
            file.write(text)
            file.close()
        else:
            path = pathlib.PurePath(path)
            base_path =path.parent
            songname = path.stem

            songname=re.sub('[^A-Za-z0-9]+', '', songname)
            finalpath = os.path.join(base_path,songname)
            file = open(finalpath + ".txt", "w",encoding='utf-8')
            file.write(text)
            file.close()
    else:
        file = open(path + ".txt", "w")
        file.write(text)
        file.close()


def get_lyrics(
        song_url,
        save=True,
        by_decade=False,
        replace=False,
        folder="songs"
):
    song = urlopen(song_url)
    soup = BeautifulSoup(song.read(), "html.parser")
    lyrics =soup.find_all(attrs={'class': None})[34].text
    # soup.find_all("div")[20].get_text()
    title = soup.find_all("b")[1].get_text().replace('"', '')
    file_title = title.replace(" ", "_")
    album = soup.find_all(class_="songinalbum_title")
    if len(album) == 1:
        album_text = album[0].get_text()
        year = int(album_text[album_text.find("(") + 1:album_text.find(")")])
        decade = str(year)[:3] + "0s"
    else:
        year = None
        decade = "others"
    if not save:
        return title, lyrics, year
    else:
        if os.path.exists(os.path.relpath(folder + "/all/")):
            save_file(path=folder + "/all/" + file_title, text=lyrics, replace=replace)
        else:
            os.makedirs(os.path.relpath(folder + "/all/"))
            save_file(path=folder + "/all/" + file_title, text=lyrics, replace=replace)
        if by_decade:
            if os.path.exists(os.path.relpath(folder + "/decades/" + decade)):
                save_file(folder + "/decades/" + decade + "/" + file_title, text=lyrics, replace=replace)
            else:
                os.makedirs(os.path.relpath(folder + "/decades/" + decade))
                save_file(folder + "/decades/" + decade + "/" + file_title, text=lyrics, replace=replace)


def scrape_artist(
        az_url,
        sleep="random",
        by_decade=True,
        replace=False,
        folder="songs"
):
    home = "https://www.azlyrics.com/"
    main_page = urlopen(az_url)
    bs = BeautifulSoup(main_page.read(), "html.parser")
    divs = bs.find_all('div', {"class": "listalbum-item"})
    urls = list()
    for d in divs:
        urls.append(home + d.a['href'].split("/", 1)[1])
    n = len(urls)
    i = 1
    for url in urls:
        get_lyrics(url, save=True, by_decade=by_decade, replace=replace, folder=folder)
        if sleep == "random":
            rt = random.randint(5, 15)
            t = 10
        else:
            rt = t = sleep
        print("Songs downloaded:", i, "/", n, " -  ETA:", round(t * (n - i) / 60, 2), "minutes")
        i += 1
        time.sleep(rt)  # This is to avoid being recognized as a bot


def get_artists(
        letter,
        home="https://www.azlyrics.com/"
):
    url = home + letter + ".html"
    page = urlopen(url)
    soup = BeautifulSoup(page.read(), "html.parser")
    links = soup.find_all("div", {"class": "row"})[1].find_all("a")
    artists_urls = list()
    artists_names = list()
    for link in links:
        artists_urls.append(home + link["href"])
        artists_names.append(link.get_text())
    return artists_urls, artists_names


def scrape_all(
        letters="all",
        sleep="random",
        by_decade=True,
        replace=False,
        folder="songs"
):
    if letters == "all":
        lets = list()
        for let in ascii_lowercase:
            lets.append(let)
        lets.append(str(19))
    else:
        lets = letters
    for let in lets:
        print("---------- LETTER:", lets, "----------")
        artists_urls, artists_names = get_artists(let)
        i = 0
        for az_url in artists_urls:
            print("\n")
            print("*** NOW SCRAPING ARTIST", str(artists_names[i]), " -  (", i + 1, "/", len(artists_urls), ") ***")
            if folder == "names":
                fold_name = artists_names[i]
            else:
                fold_name = folder
            scrape_artist(az_url=az_url, by_decade=by_decade, sleep=sleep, replace=replace, folder=fold_name)
            i += 1


# enjoy_the_silence = "https://www.azlyrics.com/lyrics/depechemode/enjoythesilence.html"
# get_lyrics(enjoy_the_silence, folder="C:\Lyrics\DM")

enya = "https://www.azlyrics.com/s/springsteen.html"
scrape_artist(enya, folder="C:\Artists\Enya")

# bruce = "https://www.azlyrics.com/s/springsteen.html"



