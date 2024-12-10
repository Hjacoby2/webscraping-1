from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

url = 'https://www.worldometers.info/coronavirus/country/us'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

req = Request(url, headers=headers)
webpage = urlopen(req).read()
soup = BeautifulSoup(webpage, 'html.parser')

print(soup.title.text)

table_rows = soup.findAll("tr")

state_death_ratio = ""
state_best_testing = ""
state_worst_testing = ""
highest_death_ratio = 0.0
best_test_ratio = 0.0
worst_test_ratio = 1000.0

def to_int(value):
    value = value.replace(",", "").strip()
    if value.isdigit():
        return int(value)
    return 0

for row in table_rows[2:53]:  
    td = row.findAll("td")
    if len(td) > 4: 
        state = td[1].text.strip('\n')

        total_cases = to_int(td[2].text)
        total_deaths = to_int(td[3].text)
        total_testing = to_int(td[4].text)
        population = to_int(td[5].text)

        death_ratio = total_deaths / total_cases if total_cases > 0 else 0
        test_ratio = total_testing / population if population > 0 else 0

        if death_ratio > highest_death_ratio:
            highest_death_ratio = death_ratio
            state_death_ratio = state

        if test_ratio > best_test_ratio:
            best_test_ratio = test_ratio
            state_best_testing = state

        if test_ratio < worst_test_ratio:
            worst_test_ratio = test_ratio
            state_worst_testing = state

print(f"State with the highest death ratio is: {state_death_ratio}")
print(f"Death ratio: {highest_death_ratio:.2%}")
print()
print(f"State with the best test ratio: {state_best_testing}")
print(f"Test ratio: {best_test_ratio:.2%}")
print()
print(f"State with the worst test ratio: {state_worst_testing}")
print(f"Test ratio: {worst_test_ratio:.2%}")
