from Proxy_List_Scrapper import Scrapper, Proxy, ScrapperException

scrapper = Scrapper(category='ALL', print_err_trace=False)
# Get ALL Proxies According to your Choice
data = scrapper.getProxies()

# Print These Scrapped Proxies
print("Scrapped Proxies:")
for item in data.proxies:
    print('{}:{}'.format(item.ip, item.port))

# Print the size of proxies scrapped
print("Total Proxies")
print(data.len)

# Print the Category of proxy from which you scrapped
print("Category of the Proxy")
print(data.category)