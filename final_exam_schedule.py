from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import csv

url = 'https://registrar.web.baylor.edu/exams-grading/fall-2024-final-exam-schedule'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
req = Request(url, headers=headers)
webpage = urlopen(req).read()

soup = BeautifulSoup(webpage, 'html.parser')

tables = soup.findAll('table')
finals_table = tables[1]

rows = finals_table.findAll("tr")

infile = open('myclasses.csv', 'r')
myclasses = csv.reader(infile)

for rec in myclasses:
    if len(rec) >= 2:  
        myclass = rec[0].strip()
        mytime = rec[1].strip()

        for row in rows[1:]:  
            td = row.findAll('td')
            if len(td) >= 4:  
                sch_class = td[0].text.strip()
                sch_time = td[1].text.strip()
                exam_day = td[2].text.strip()
                exam_time = td[3].text.strip()

                if sch_class == myclass and sch_time == mytime:
                    print(f"{myclass},{mytime},{exam_day}, {exam_time}")
