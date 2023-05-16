from Proxy_List_Scrapper import Scrapper, Proxy, ScrapperException



def get_list_of_proxies():
    proxy_list = []
    # SSL = 'https://www.sslproxies.org/',
    # GOOGLE = 'https://www.google-proxy.net/',
    # ANANY = 'https://free-proxy-list.net/anonymous-proxy.html',
    # UK = 'https://free-proxy-list.net/uk-proxy.html',
    # US = 'https://www.us-proxy.org/',
    # NEW = 'https://free-proxy-list.net/',
    # SPYS_ME = 'http://spys.me/proxy.txt',
    # PROXYSCRAPE = 'https://api.proxyscrape.com/?request=getproxies&proxytype=all&country=all&ssl=all&anonymity=all',
    # PROXYNOVA = 'https://www.proxynova.com/proxy-server-list/'
    # PROXYLIST_DOWNLOAD_HTTP = 'https://www.proxy-list.download/HTTP'
    # PROXYLIST_DOWNLOAD_HTTPS = 'https://www.proxy-list.download/HTTPS'
    # PROXYLIST_DOWNLOAD_SOCKS4 = 'https://www.proxy-list.download/SOCKS4'
    # PROXYLIST_DOWNLOAD_SOCKS5 = 'https://www.proxy-list.download/SOCKS5'
    ALL = 'ALL'
    scrapper = Scrapper(category='ANANY', print_err_trace=False)
# Get ALL Proxies According to your Choice
    data = scrapper.getProxies()

# Print These Scrapped Proxies
#print("Scrapped Proxies:")
    for item in data.proxies:
        proxy_list.append('{}:{}'.format(item.ip, item.port))
        #print('{}:{}'.format(item.ip, item.port))
    return proxy_list

# Print the size of proxies scrapped
#print("Total Proxies")
#print(data.len)

# Print the Category of proxy from which you scrapped
#print("Category of the Proxy")
#print(data.category)