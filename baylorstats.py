import requests
from bs4 import BeautifulSoup
import plotly.express as px #i researched plotly.express and found that it has much simpler code than plotly.graph_objs

def sort_by_attendance(item):
    return item[1]

def fetch_year_stats(years):
    year_stats = {
        'Scoring Points/Game': {},
        'Passing Yards': {},
        '3rd down conversion %': {},
        'Field goals success %': {}
    }

    for year in years:
        url = f'https://cfbstats.com/{year}/team/51/index.html'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        scoring_points = float(soup.find('td', string='Scoring:  Points/Game').find_next('td').text.strip())
        passing_yards = int(soup.find('td', string='Passing:  Yards').find_next('td').text.strip())
        third_down_conversions = float(soup.find('td', string='3rd Down Conversions: Conversion %').find_next('td').text.strip().strip('%'))
        field_goal_percentage = float(soup.find('td', string='Field Goals:  Success %').find_next('td').text.strip().strip('%'))

        year_stats['Scoring Points/Game'][year] = scoring_points
        year_stats['Passing Yards'][year] = passing_yards
        year_stats['3rd down conversion %'][year] = third_down_conversions
        year_stats['Field goals success %'][year] = field_goal_percentage
    return year_stats

def find_best_worst(stats):
    best_year = max(stats, key=stats.get)
    worst_year = min(stats, key=stats.get)
    return best_year, stats[best_year], worst_year, stats[worst_year]

url = 'https://cfbstats.com/2024/team/51/index.html'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

tables = soup.findAll('table')
attendance_data = []

attendance_table = tables[1]
rows = attendance_table.findAll("tr")

for row in rows:
    cols = row.find_all('td')
    if len(cols) > 4:
        opponent = cols[1].text.strip()
        opponent = opponent.replace('@', '').strip()
        
        attend = cols[4].text.strip().replace(',', '')
        if attend.isdigit():
            attend = int(attend)
            attendance_data.append((opponent, attend))

attendance_data.sort(key=sort_by_attendance, reverse=True)
top_5_teams = attendance_data[:5]

opponents = [team[0] for team in top_5_teams]
attendances = [team[1] for team in top_5_teams]

fig = px.bar(x=opponents, y=attendances, labels={'x': 'Opponent', 'y': 'Attendance'},
             title="Biggest Rivalry based on Attendance", color=attendances)

fig.update_layout(
    plot_bgcolor='gold',
    paper_bgcolor='gold',
)

fig.update_traces(marker=dict(color='green'))

fig.show()

years = range(2016, 2024)
year_stats = fetch_year_stats(years)

print(year_stats)

for stat, stats in year_stats.items():
    best_year, best_value, worst_year, worst_value = find_best_worst(stats)
    print(f"{stat}:")
    print(f"  Best Year: {best_year} with {best_value}")
    print(f"  Worst Year: {worst_year} with {worst_value}")
    print()
