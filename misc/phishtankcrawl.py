import requests
from bs4 import BeautifulSoup
import pandas as pd
import threading
import time

counter = 22005
long_counter = 15578
extra_counter = [22005, 22019]

url = "https://phishtank.com/phish_search.php"
page_amt = 65000
columns = ["url", "live"]
url_df = pd.DataFrame(columns=columns)

for page in range(long_counter, page_amt):
    try:
        print("[*] Processing page " + str(page))
        params = {"page": page, "valid": "y", "Search": "Search"}
        resp = requests.get(url, params=params)
        html_soup = BeautifulSoup(resp.text, "html.parser")
        table_data = html_soup.find_all('td')
        for item in range(1, len(table_data), 5):
            phish_link = table_data[item].contents[0]
            if b'\xc2\xa0' in phish_link.encode():
                continue
            elif "..." in phish_link:
                full_link = "https://phishtank.com/" + table_data[item-1].a['href']
                resp = requests.get(full_link)
                link_soup = BeautifulSoup(resp.text, "html.parser")
                full_phish_link = link_soup.find_all('span')[2].get_text()
                if "Ray ID" in full_phish_link:
                    print("[x] Limit at page " + str(page))
                    time.sleep(500)
                df = url_df.append({"url": full_phish_link, "live": 1 if "ONLINE" in table_data[item+3].contents[0] else 0}, ignore_index=True)
                df.to_csv("phish_long.csv", mode='a', header=False, index=False)
                time.sleep(0.2)
            else:
                continue
                df = url_df.append({"url": phish_link, "live": 1 if "ONLINE" in table_data[item+3].contents[0] else 0}, ignore_index=True)
                df.to_csv("phish_clean.csv",mode='a', header=False, index=False)
    except:
        pass
#
# df.to_csv("phish.csv", index=False)
