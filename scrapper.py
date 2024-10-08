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
# import proxies
import requests
import proxy_list_scrapper as pps
import psycopg2


# def get_proxies(number, port, p, country):
#     r = requests.post('http://spys.one/en/https-ssl-proxy/',  data = {'xpp': 5, 'xf4': number})
#     soup = BeautifulSoup(r.content, 'lxml')
#     proxies = [':'.join([p.findall(i.text)[0], port]) for i in soup.select('table table tr:has(.spy14:contains("' + country + '")) td:has(script) .spy14')]
#     return proxies
#
# ports = ['3128', '8080', '80']
# p = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})document')
# proxies = []
#
# for number, port in enumerate(ports,1):
#     proxies+=get_proxies(number, port, p, 'United States')
#
# print(proxies)

def get_http_proxy_list():
    proxy_url = "https://spys.one/en/free-proxy-list/"
    req = urllib.request.Request(proxy_url, headers={'User-Agent': "Magic Browser"})
    con = urllib.request.urlopen(req)
    soup = BeautifulSoup(con.read(), "html.parser")
    tables = soup.findAll("table")
    # s = dryscrape.Session()
    # s.visit(proxy_url)
    # df = pd.read_html(s.body())[5]
    # df.head()
    for table in tables:
        # if table.findParent("table") is None:
        rowsLen = len(table.findAll(lambda tag: tag.name == 'tr' and tag.findParent('table') == table))
        print(rowsLen)
        if rowsLen > 30:
            print(table)
            df = pd.read_html(str(table), header=0)[0]
            df[['A', 'B']] = df['Free proxy list. Open proxy servers. Shared proxies list.'].str.split('document.',
                                                                                                       expand=True)
            print(df)


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
        sock = urllib.request.urlopen('https://www.google.com')
    except urllib.error.HTTPError as e:
        print('Error code: ', e.code)
        return e.code
    except Exception as detail:

        print("ERROR:", detail)
        return 1
    return 0


def get_valid_proxy(proxy_list):  # format of items e.g. '128.2.198.188:3124'

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
            base_path = path.parent
            songname = path.stem

            songname = re.sub('[^A-Za-z0-9_]', '', songname)
            finalpath = os.path.join(base_path, songname)
            file = open(finalpath + ".txt", "w", encoding='utf-8')
            file.write(text)
            file.close()
    else:
        file = open(path + ".txt", "w")
        file.write(text)
        file.close()


def get_lyrics(
        song_url,
        artist_name,
        current_proxy,
        save=True,
        by_decade=False,
        replace=False,
        folder="songs"
):

    time.sleep(15)

        # try:
        #     response = requests.get(song_url, proxies={'https': current_proxy}, timeout=200)
        #     if response.status_code == 200:
        #         break
        # except:
        #     pass
    # song = urlopen(song_url)
    request = urllib.request.Request(song_url)
    request.set_proxy(current_proxy, 'https')
    song = urllib.request.urlopen(request)
    soup = BeautifulSoup(song.read(), "html.parser")
    lyrics = soup.find_all(attrs={'class': None})[34].text
    lyrics = lyrics.lstrip()
    if len(lyrics) > 100:
        # soup.find_all("div")[20].get_text()
        title = soup.find_all("b")[1].get_text().replace('"', '').replace("/","_").replace("\\","")
        file_title = title.replace(" ", "_")
        album = soup.find_all(class_="songinalbum_title")
        if len(album) >= 1:
            album_text = album[0].get_text()
            if (album_text[album_text.find("(") + 1:album_text.find(")")]).isnumeric():
                year = int(album_text[album_text.find("(") + 1:album_text.find(")")])
                decade = str(year)[:3] + "0s"
            else:
                print(album_text)
        else:

            year = None
            decade = "others"
        if not save:
            return title, lyrics, year
        else:
            try:
                # Create a cursor object
                cur = conn.cursor()
                # Define the SQL query and the parameter values
                query = "INSERT INTO songs (artist, decade, song_title, lyrics) VALUES (%s, %s, %s, %s)"
                params = (artist_name, decade, title, lyrics)

                # Execute the query with the parameter values
                cur.execute(query, params)

                # Commit the changes to the database
                conn.commit()

                # Close the cursor and the database connection
                cur.close()


            except:
                pass

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
        folder="songs",
        artist_name = "N.A"
):
    home = "https://www.azlyrics.com/"
    while True:
        proxy = random.choice(candidate_proxies)
        try:
            print(f"trying proxy : {proxy}", end=" ")
            response = requests.get(az_url, proxies={'https': proxy}, timeout=32)

            if response.status_code == 200:
                time.sleep(3)
                print("\n Initialization of song lyrics download")
                url = az_url
                request = urllib.request.Request(url)
                request.set_proxy(proxy, 'https')
                main_page = urllib.request.urlopen(request)
                bs = BeautifulSoup(main_page.read(), "html.parser")
                divs = bs.find_all('div', {"class": "listalbum-item"})
                urls = list()
                for d in divs:
                    try:
                        urls.append(home + d.a['href'].split("/", 1)[1])
                    except:
                        pass

                i = 1
                folder_path = os.path.join(folder, "all")
                if os.path.isdir(folder_path):
                    current_downloaded_files = os.listdir(folder_path)
                    empty_files = {f for f in current_downloaded_files if
                                   os.stat(os.path.join(folder, "all", f)).st_size == 0}
                    downloaded_files = set(current_downloaded_files) - empty_files
                    downloaded_files = [s.split('.')[0].replace('_', '').lower() for s in list(downloaded_files)]
                    urls_to_download = [url for url in urls if not any(word in url for word in
                                                                       [s.split('.')[0].replace('_', '').lower() for s
                                                                        in list(downloaded_files)])]
                else:
                    urls_to_download = urls

                n = len(urls_to_download)
                for url in urls_to_download:
                    get_lyrics(url,artist_name, proxy, save=True, by_decade=by_decade, replace=replace, folder=folder)
                    if sleep == "random":
                        rt = random.randint(5, 15)
                        t = 10
                    else:
                        rt = t = sleep
                    print("Songs downloaded:", i, "/", n, " -  ETA:", round(t * (n - i) / 60, 2), "minutes",
                          " lyric : ", url)
                    i += 1
                    time.sleep(rt)  # This is to avoid being recognized as a bot
                break
            else:
                response = requests.get(az_url, proxies={'http': proxy}, timeout=20)
                url = az_url
                request = urllib.request.Request(url)
                request.set_proxy(proxy, 'http')
                main_page = urllib.request.urlopen(request)
                bs = BeautifulSoup(main_page.read(), "html.parser")
                divs = bs.find_all('div', {"class": "listalbum-item"})
                urls = list()
                for d in divs:
                    urls.append(home + d.a['href'].split("/", 1)[1])

                i = 1
                current_downloaded_files = os.listdir(os.path.join(folder, "all"))
                empty_files = {f for f in current_downloaded_files if
                               os.stat(os.path.join(folder, "all", f)).st_size == 0}
                downloaded_files = set(current_downloaded_files) - empty_files
                downloaded_files = [s.split('.')[0].replace('_', '').lower() for s in list(downloaded_files)]
                urls_to_download = [url for url in urls if not any(
                    word in url for word in [s.split('.')[0].replace('_', '').lower() for s in list(downloaded_files)])]
                n = len(urls_to_download)
                for url in urls_to_download:
                    get_lyrics(url, proxy, save=True, by_decade=by_decade, replace=replace, folder=folder)
                    if sleep == "random":
                        rt = random.randint(5, 15)
                        t = 10
                    else:
                        rt = t = sleep
                    print("Songs downloaded:", i, "/", n, " -  ETA:", round(t * (n - i) / 60, 2), "minutes",
                          " lyric : ", url)
                    i += 1
                    time.sleep(rt)  # This is to avoid being recognized as a bot
            break


        except:
            print(f"fail on using proxy {proxy}")
            pass


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


# candidate_proxies = proxies.get_list_working_proxies()
# https://spys.one/en/free-proxy-list/
# candidate_proxies = ['206.189.234.208:8080','206.189.234.208:8080','34.75.202.63:80','135.181.255.160:8080','87.236.197.231:3128']
# candidate_proxies = ['206.189.234.208:8080','87.236.197.231:3128','65.108.48.232:8080       ']
# Initiate Database Connection
conn = psycopg2.connect(database="aclepmym", user="aclepmym", password="K588WhHB-Mvpn-i_LEFZ5IcbZ4ZeOba7",
                        host="balarama.db.elephantsql.com", port="5432")

print("Opened database successfully")

candidate_proxies = pps.get_list_of_proxies()
list_of_artists = ['https://www.azlyrics.com/w/whitesnake.html','https://www.azlyrics.com/d/depeche.html',
                   'https://www.azlyrics.com/p/petshop.html','https://www.azlyrics.com/j/journey.html']
for artist in list_of_artists:
    artist_to_scrape = artist # "https://www.azlyrics.com/w/whitesnake.html"
    artist_name = artist.split("/")[-1].split(".")[0]
    save_path = os.path.join(r"C:\Artists",artist_name)
    #scrape_artist(artist_to_scrape, folder=f"C:\Artists\\whitesnake",artist_name=artist_name)
    scrape_artist(artist_to_scrape, folder=save_path, artist_name=artist_name)
conn.close()
# only_time = "https://www.azlyrics.com/lyrics/enya/onlytime.html"
# get_lyrics(only_time, folder="/Volumes/Teras/Information Retrieval/Lyrics/Only Time")
