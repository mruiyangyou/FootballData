import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import re

class FootballData(object):

    base_url = 'https://www.football-data.co.uk'
    country_list = ['england']
    league_list = ['Premier League']
    feature_list = ['Div', 'Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG',
       'FTR', 'HTHG', 'HTAG', 'HTR', 'Referee', 'HS', 'AS', 'HST', 'AST', 'HF',
       'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR']
    

    def __init__(self, country, league) -> None:
        if country not in self.country_list or league not in self.league_list:
            raise ValueError('The name of the league or country may wrong. Please check the eligible name!')
        self.country = country
        self.league = league
        target_url = os.path.join(self.base_url, str(self.country).lower() + 'm.php')
        page = requests.get(target_url)
        self.soup = BeautifulSoup(page.content, 'html.parser')
        
        
    
    @classmethod
    def get_data_intro(cls):
        '''
        Return the notes of feature name for the data set
        '''
        
        fpath = os.path.join(os.path.dirname(__file__), '../notes')
    
        match_data = pd.read_csv(os.path.join(fpath, 'resultsdata_notes.txt'), sep = ' = ', header=None, names = ['Feature Name', 'Explainations'])
        stats_data = pd.read_csv(os.path.join(fpath, 'matchstatistics_notes.txt'), sep = ' = ', header=None, names = ['Feature Name', 'Explainations'])
        return match_data, stats_data



    def scrape_one_season(self, year):
        season = str(int(year))[-2:] + str(int(year)+1)[-2:]
        data_url = self.soup.find('a', href = re.compile(season), string = self.league).get('href')
        if not isinstance(data_url, str):
            raise ValueError('Please check season, year or league input!')
        else: 
            # df = pd.read_csv(os.path.join(self.base_url, data_url)).loc[:, self.feature_list]
            try:
                df = pd.read_csv(os.path.join(self.base_url, data_url))
            except pd.errors.ParserError:
                df = pd.read_csv(os.path.join(self.base_url, data_url), on_bad_lines = 'skip')
                print(f'Data Loss on Year {year}')
            except UnicodeDecodeError:
                try:
                    df = pd.read_csv(os.path.join(self.base_url, data_url), encoding= 'unicode_escape')
                except pd.errors.ParserError:
                    df = pd.read_csv(os.path.join(self.base_url, data_url), on_bad_lines = 'skip', encoding= 'unicode_escape')
                    print(f'Data Loss on Year {year}')
            df = df.loc[:, self.feature_list]
            league_df = pd.DataFrame([self.league] * df.shape[0], columns = ['League'])
            return pd.concat([league_df, df], axis = 1)

    def scrape_fixture(self, start_year, end_year):
        if isinstance(start_year, int) and isinstance(end_year, int):
            res_df = pd.DataFrame(columns=['1'] * 25)
            for i in range(start_year, end_year+1):
                season_df = self.scrape_one_season(i)
                season = pd.DataFrame([('-').join([str(i), str(i + 1)])] * season_df.shape[0], columns=['Season'])
                season_df = pd.concat([season, season_df], axis= 1)
                if i == start_year:
                    res_df.columns = season_df.columns 
                res_df = pd.concat([res_df, season_df])
            return res_df
        else:
            raise ValueError('Check input Year. Both must be valid interger!')
    
    def scrape_match_data(self, club, start_year, end_year = None):
        if (isinstance(club, str) and isinstance(start_year, int) and isinstance(end_year, int)) or (isinstance(club, str) and isinstance(start_year, int) and end_year == None):
            if not end_year:
                res_df = self.scrape_one_season(start_year)
            else:
                res_df =  self.scrape_fixture(start_year, end_year)
            return res_df.loc[(res_df['HomeTeam'] == club)| (res_df['AwayTeam'] == club)]
        else:
            raise ValueError('Please check the input type!')
        