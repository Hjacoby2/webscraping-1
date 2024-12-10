from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

url = 'https://www.webull.com/quote/us/gainers'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

req = Request(url, headers=headers)

webpage = urlopen(req).read()

soup = BeautifulSoup(webpage, 'html.parser')

print(soup.title.text)

stock_data = soup.findAll("div", attrs={"class": "table-cell"})

counter = 1

for x in range(5): 
    name = stock_data[counter].text.strip()
    change_text = stock_data[counter + 2].text.strip()
    if change_text != "": 
        change = float(change_text.strip('+').strip('%')) / 100
    else:
        change = 0.0  

    last_price = float(stock_data[counter + 3].text.strip().replace(",", ""))  
    previous_price = round(last_price / (1 + change), 2)

    print()
    print(f"Company Name: {name}")
    print(f"Change: {change: .2%}")
    print(f"Price: {last_price}")
    print(f"Previous price: {previous_price}")
    print()

    counter += 11