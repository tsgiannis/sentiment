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
import random
import urllib
#import proxies
import requests

def set_http_proxy(proxy):
    if proxy == None:  # Use system default setting
        proxy_support = urllib.request.ProxyHandler()
    elif proxy == '':  # Don't use any proxy
        proxy_support = urllib.request.ProxyHandler({})
    else:  # Use proxy
        proxy_support = urllib.request.ProxyHandler({'http': '%s' % proxy, 'https': '%s' % proxy})
    opener = urllib.request.build_opener(proxy_support)
    urllib.request.install_opener(opener)


def is_bad_proxy(pip):
    try:
        proxy_handler = urllib.request.ProxyHandler({'http': pip})
        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        sock=urllib.request.urlopen('https://www.google.com')
    except urllib.error.HTTPError as e:
        print('Error code: ', e.code)
        return e.code
    except Exception as detail:

        print( "ERROR:", detail)
        return 1
    return 0




def get_valid_proxy(proxy_list): #format of items e.g. '128.2.198.188:3124'

    proxies = random.sample(proxy_list, 2)
    for proxy in proxies:
        if not is_bad_proxy(proxy):
            return proxy



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
            songname = re.sub('[^A-Za-z0-9_]', '', songname)
            finalpath = os.path.join(base_path, songname)

            file = open(finalpath + "_2" + ".txt", "w")
            file.write(text)
            file.close()
        else:
            path = pathlib.PurePath(path)
            base_path =path.parent
            songname = path.stem

            songname=re.sub('[^A-Za-z0-9_]', '', songname)
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
        #proxy = "174.138.184.82:37737"

):
    while True :
        time.sleep(15)
        proxy = random.choice(candidate_proxies)
        try:
            response = requests.get(song_url, proxies={'https': proxy}, timeout=200)
            if response.status_code == 200:
                break
        except:
            pass
    #song = urlopen(song_url)
    request = urllib.request.Request(song_url)
    request.set_proxy(proxy, 'https')
    song = urllib.request.urlopen(request)
    soup = BeautifulSoup(song.read(), "html.parser")
    lyrics =soup.find_all(attrs={'class': None})[34].text
    # soup.find_all("div")[20].get_text()
    title = soup.find_all("b")[1].get_text().replace('"', '')
    file_title = title.replace(" ", "_")
    album = soup.find_all(class_="songinalbum_title")
    if len(album) == 1:
        album_text = album[0].get_text()
        if (album_text[album_text.find("(") + 1:album_text.find(")")]).isnumeric():
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
    while True :
        proxy = random.choice(candidate_proxies)
        try:
            response = requests.get(az_url, proxies={'https': proxy}, timeout=50)
            if response.status_code == 200:
                break
        except:
            pass

    url = az_url
    request = urllib.request.Request(url)
    request.set_proxy(proxy,'https')
    main_page =urllib.request.urlopen(request)
    bs = BeautifulSoup(main_page.read(), "html.parser")
    divs = bs.find_all('div', {"class": "listalbum-item"})
    urls = list()
    for d in divs:
        urls.append(home + d.a['href'].split("/", 1)[1])
    n = len(urls)
    i = 1
    for url in urls:
        current_proxy = random.choice(candidate_proxies)
        get_lyrics(url, save=True, by_decade=by_decade, replace=replace, folder=folder)
        if sleep == "random":
            rt = random.randint(5, 15)
            t = 10
        else:
            rt = t = sleep
        print("Songs downloaded:", i, "/", n, " -  ETA:", round(t * (n - i) / 60, 2), "minutes"," lyric : " ,url)
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

# enya = "https://www.azlyrics.com/e/enya.html"
# scrape_artist(enya, folder="/Volumes/Teras/Information Retrieval/Artists/Enya")
# candidate_proxies = ['http://proxy1.example.com:1234',
#                      'http://proxy2.example.com:1234',
#                      'http://proxy3.example.com:1234']


#candidate_proxies = proxies.get_list_working_proxies()
#https://spys.one/en/free-proxy-list/
candidate_proxies = ['206.189.234.208:8080','206.189.234.208:8080','34.75.202.63:80','135.181.255.160:8080','87.236.197.231:3128']
candidate_proxies = ['206.189.234.208:8080','87.236.197.231:3128','65.108.48.232:8080       ']
enya = "https://www.azlyrics.com/s/springsteen.html"
scrape_artist(enya, folder="C:\Artists\Enya")

only_time = "https://www.azlyrics.com/lyrics/enya/onlytime.html"
get_lyrics(only_time, folder="/Volumes/Teras/Information Retrieval/Lyrics/Only Time")


