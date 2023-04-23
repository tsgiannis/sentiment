import requests
from bs4 import BeautifulSoup

# URL of the website to scrape
#url = 'https://www.proxy-list.download/api/v1/get?type=http'

def get_list_working_proxies():

    # URL of the website to scrape
    url = 'https://www.proxy-list.download/api/v1/get?type=https'

    # Retrieve the webpage content
    response = requests.get(url)

    # Parse the response text as a list of proxies
    proxies = response.text.split('\r\n')

    # Check if each proxy is working by making a test request
    working_proxies = []
    for proxy in proxies:
        try:
            response = requests.get('https://free-proxy-list.net', proxies={'https': proxy}, timeout=50)
            if response.status_code == 200:
                working_proxies.append(proxy)
        except:
            pass

    # Print the list of working proxies
    #print(working_proxies)
    return working_proxies
