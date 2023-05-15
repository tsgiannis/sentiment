import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome("chromedriver.exe", options=options)

url_req = "https://spys.one/en/https-ssl-proxy/"
driver.get(url_req)
time.sleep(5)
soup = BeautifulSoup(driver.page_source, "lxml")

driver.close()

trs = soup.find_all('tr', {'class': ['spy1']})
for i in trs[1:]:
    print(i.select_one('td').text.strip())