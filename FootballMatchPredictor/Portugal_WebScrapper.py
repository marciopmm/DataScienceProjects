import pandas as pd
import requests
import time
import datetime
from bs4 import BeautifulSoup as bs
from io import StringIO

class Portugal_WebScrapper:
    def __init__(self, csv_path):
        self.csv_path = csv_path

    def get_data(self):
        todayYear = datetime.datetime.now().year
        years = list(range(todayYear,2019,-1))
        all_matches = []

        standings_url = "https://fbref.com/pt/comps/32/{ano}-{ano1}/{ano}-{ano1}-Primeira-Liga-estatisticas"

        for year in years:
            data = requests.get(standings_url.replace("{ano}", str(year-1)).replace("{ano1}", str(year)))
            if data.status_code != 200:
                print(f'{year-1}-{year} - Temporada Não Disponível')
                continue;
            soup = bs(data.text, features="lxml")
            standings_table = soup.select('table.stats_table')[0]

            links = [l.get('href') for l in standings_table.find_all('a')]
            links = [l for l in links if '/equipes/' in l]
            team_urls = [f'https://fbref.com{l}' for l in links]

            # previous_season = soup.select('a.prev')[0].get('href')
            # standings_url = f"https://fbref.com/{previous_season}"

            for team_url in team_urls:
                team_name = team_url.split('/')[-1].replace('-Estatisticas', '').replace('-', ' ')

                data = requests.get(team_url)
                matches = pd.read_html(StringIO(data.text), match='Resultados e Calendários')[0]

                soup = bs(data.text, features="lxml")
                links = [l.get('href') for l in soup.find_all('a')]
                links = [l for l in links if l and '/partidas/all_comps/shooting/' in l]
                print(f'https://fbref.com{links[0]}')
                data = requests.get(f'https://fbref.com{links[0]}')
                shooting = pd.read_html(StringIO(data.text), match='Chutes')[0]
                shooting.columns = shooting.columns.droplevel()

                try:
                    team_data = matches.merge(shooting[['Data', 'TC', 'CaG', 'Dist', 'G/Sh', 'FK', 'PB', 'PT']], on='Data')
                except ValueError:
                    continue

                team_data = team_data[team_data['Camp.'] == 'Primeira Liga']
                team_data['Temporada'] = f'{year}-{year+1}'
                team_data['Time'] = team_name
                all_matches.append(team_data)
                time.sleep(6)

        match_df = pd.concat(all_matches, ignore_index=True)
        match_df['Camp'] = match_df['Camp.']
        match_df = match_df.drop('Camp.', axis='columns')
        match_df.columns = [c.lower() for c in match_df.columns]
        match_df.to_csv(self.csv_path)

        print(f'Saved to CSV at {self.csv_path}')