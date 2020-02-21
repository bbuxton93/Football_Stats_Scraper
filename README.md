
# Football Data Scraper

This was built as a tool to pull out Fantasy and other Stats from the below websites. Code is not perfect, optimized or perfectly annotated - but hopefully is is helpful! The extractions were used to build an interactive Qliksense application.
* https://www.pro-football-reference.com - This is the main extraction tool
* https://teamcolorcodes.com/ - This is for color codes and logos
* https://www.youtube.com/ - This was to pull out video URLS




```python
# Full Real Stats

from bs4 import BeautifulSoup
import pandas as pd
import requests
import numpy as np

# set url and year. maxp is # of players to load from table
url = 'https://www.pro-football-reference.com'
year = 2019
maxp = 300

# grab fantasy players. First block grabs urls from table
r = requests.get(url + '/years/' + str(year) + '/fantasy.htm')
soup = BeautifulSoup(r.content, 'html.parser')
parsed_table = soup.find_all('table')[0]

df = []
tdf = []
# r_img = requests.get('https://www.pro-football-reference.com/players/M/McCaCh01.htm')
# soup_img = BeautifulSoup(r_img.content, 'html.parser')
# parsed_img= soup_img.find_all('img')[1]
# url= parsed_img.get('src')
# print(url)

# first 2 rows are col headers
for i, row in enumerate(parsed_table.find_all('tr')[2:]):
    if i % 10 == 0:
        print(i, end=' \n')
    if i >= maxp:
        print('\nComplete.')
        break

    try:
        # stub is the piece of URL for each player
        dat = row.find('td', attrs={'data-stat': 'player'})
        name = dat.a.get_text()
        stub = dat.a.get('href')
        stub = stub[:-4] + '/fantasy/' + str(year)
        #print(url + stub)
        # find position of player
        pos = row.find('td', attrs={'data-stat': 'fantasy_pos'}).get_text()
        # read in html - our table is the first table in the webpage
        tdf = pd.read_html(url + stub)[0]
        # grab the correct column index for the columns we want
        tdf.columns = tdf.columns.get_level_values(-1)
        print(len(tdf.columns.tolist()))
        print(tdf.columns.tolist())
        #r_img = requests.get(url + stub)
        #soup_img = BeautifulSoup(r_img.content, 'html.parser')

        # setup for dynamic renaming of columns
        column_list = []
        # below grabs the html info from the table. We use this to get column names and also image url
        r2 = requests.get(url+stub)
        soup2 = BeautifulSoup(r2.content, 'html.parser')
        parsed_img = soup2.find_all('img')[1]
        # these pieces are finding the corrent html piece we need. takes some sleuthing
        parsed_table2 = soup2.find_all('table')[0]
        table = parsed_table2.find_all('tr')[2]

        # print(table)
        for th in table.find_all('th')[0:8]:
            # print(th)
            # header='DESC'
            # colname=
            column_name = th.get_text()
            column_list.append(column_name)
            # print(column_name)

        for th in table.find_all('th')[8:]:
            # print(th)
            if 'in_10' in th['data-stat']:
                top_head = 'Inside 10_'
            else:
                top_head = ''
            header = th['data-over-header']
            # print(len(header))
            colname = th.get_text()
            column_name = top_head+header+'_'+colname

            column_list.append(column_name)
            print(column_name)
        print(len(column_list))
        # print(column_list)
        #tdf['img_URL']   = parsed_img.get('src')


#         # fix the away/home column

        # drop all intermediate stats

        # drop "Total" row
        tdf = tdf.query('Date != "Total"')

        # add other info

#         parsed_img= soup_img.find_all('img')[1]
#         #print(parsed_img)
#         tdf['img_URL']= parsed_img.get('src')
        tdf.columns = column_list
        tdf['Name'] = name
        tdf['Position'] = pos
        tdf['Season'] = year
        tdf = tdf.rename(columns={'': 'Away'})
        tdf['Away'] = [1 if r == '@' else 0 for r in tdf['Away']]
#         #print(tdf.columns)
        tdf['img_URL'] = parsed_img.get('src')
        # print(tdf.columns)
        # print(tdf.columns)
        df.append(tdf)

    except:
        pass
df = pd.concat(df, sort=False)
# [x.replace(",", "").replace(".", "").replace(" ","")
#  for line in file for word in line]
df.to_csv('fantasy2019_1.csv')
```

    0 
    39
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    39
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    35
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    35
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    27
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    27
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    10 
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    39
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    39
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    20 
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    33
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    33
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    30 
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    39
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    39
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    40 
    39
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    39
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    27
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    27
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    35
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    35
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    50 
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    33
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    33
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    60 
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    27
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    27
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    70 
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    80 
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    90 
    39
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    39
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    100 
    23
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    23
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    27
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    27
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    110 
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    27
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    27
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    120 
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    21
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    21
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    21
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    21
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    27
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    27
    130 
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    140 
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    27
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    27
    27
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    27
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    150 
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    23
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    23
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    21
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    21
    33
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    33
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    160 
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    27
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    27
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    27
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    27
    23
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    23
    170 
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    180 
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    27
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    27
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    27
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    27
    190 
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    23
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    23
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    23
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    23
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    200 
    39
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    39
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    23
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    23
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    210 
    35
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    35
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    220 
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    27
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    27
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    21
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    21
    230 
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    27
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    27
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    27
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    27
    27
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    27
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    240 
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    23
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    23
    27
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    27
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    250 
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    23
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    23
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    21
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    21
    260 
    27
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    27
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    33
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    33
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    270 
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    23
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    23
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    17
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    17
    280 
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Cmp', 'Att', 'Yds', 'TD', 'Cmp', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Passing_Cmp
    Passing_Att
    Passing_Yds
    Passing_TD
    Inside 10_Passing_Cmp
    Inside 10_Passing_Att
    Inside 10_Passing_Yds
    Inside 10_Passing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    27
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    27
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    31
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    31
    21
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    21
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    23
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    23
    290 
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    17
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    17
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    27
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Att', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Att', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Rushing_Att
    Rushing_Yds
    Rushing_TD
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Rushing_Att
    Inside 10_Rushing_Yds
    Inside 10_Rushing_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    27
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    25
    ['Rk', 'G#', 'Date', 'Tm', 'Unnamed: 4_level_2', 'Opp', 'Result', 'Pos', 'Tgt', 'Rec', 'Yds', 'TD', 'Tgt', 'Rec', 'Yds', 'TD', 'Num', 'Pct', 'Num', 'Pct', 'Num', 'Pct', 'FantPt', 'DKPt', 'FDPt']
    Receiving_Tgt
    Receiving_Rec
    Receiving_Yds
    Receiving_TD
    Inside 10_Receiving_Tgt
    Inside 10_Receiving_Rec
    Inside 10_Receiving_Yds
    Inside 10_Receiving_TD
    Off._Num
    Off._Pct
    Def._Num
    Def._Pct
    ST_Num
    ST_Pct
    Fantasy_FantPt
    Fantasy_DKPt
    Fantasy_FDPt
    25
    300 
    
    Complete.
    


```python
# grab fantasy players
r = requests.get(url + '/years/' + str(year) + '/fantasy.htm')
soup = BeautifulSoup(r.content, 'html.parser')
parsed_table = soup.find_all('table')[0]

df = []
tdf = []
# r_img = requests.get('https://www.pro-football-reference.com/players/M/McCaCh01.htm')
# soup_img = BeautifulSoup(r_img.content, 'html.parser')
# parsed_img= soup_img.find_all('img')[1]
# url= parsed_img.get('src')
# print(url)

# first 2 rows are col headers
for i, row in enumerate(parsed_table.find_all('tr')[2:]):
    if i % 10 == 0:
        print(i, end=' \n')
    if i >= maxp:
        print('\nComplete.')
        break

    try:
        dat = row.find('td', attrs={'data-stat': 'player'})
        name = dat.a.get_text()
        stub = dat.a.get('href')
        stub = stub[:-4] + '/gamelog/' + str(year)
        #print(url + stub)
        pos = row.find('td', attrs={'data-stat': 'fantasy_pos'}).get_text()
        tdf = pd.read_html(url + stub)[0]
        tdf.columns = tdf.columns.get_level_values(-1)
        # print(len(tdf.columns.tolist()))
        # print(tdf.columns.tolist())
        #r_img = requests.get(url + stub)
        #soup_img = BeautifulSoup(r_img.content, 'html.parser')

        # setup for dynamic renaming of columns
        column_list = []
        r2 = requests.get(url+stub)
        soup2 = BeautifulSoup(r2.content, 'html.parser')
        parsed_img = soup2.find_all('img')[1]
        parsed_table2 = soup2.find_all('table')[0]
        table = parsed_table2.find_all('tr')[1]

        # print(table)
        for th in table.find_all('th')[0:10]:
            # print(th)
            # header='DESC'
            # colname=
            column_name = th.get_text()
            column_list.append(column_name)
            # print(column_name)

        for th in table.find_all('th')[10:]:
            # print(th)
            header = th['data-over-header']
            # print(len(header))
            colname = th.get_text()
            column_name = top_head+header+'_'+colname

            column_list.append(column_name)
            # print(column_name)
        # print(len(column_list))
        # print(column_list)
        #tdf['img_URL']   = parsed_img.get('src')


#         # fix the away/home column

         # drop all intermediate stats

        # drop "Total" row
        tdf = tdf.query('Date != "Total"')

        # add other info
        tdf = tdf.rename(columns={'Unnamed: 6_level_1': 'Away'})
#         parsed_img= soup_img.find_all('img')[1]
#         #print(parsed_img)
#         tdf['img_URL']= parsed_img.get('src')
        tdf = tdf.loc[:, ~tdf.columns.str.contains('Unnamed', case=False)]
        tdf = tdf[~tdf.Date.str.contains("Games")]
        # print(tdf.columns)
        tdf.columns = column_list
        tdf = tdf.rename(columns={'': 'Away'})
        tdf['Name'] = name
        tdf['Position'] = pos
        tdf['Season'] = year

        tdf['Away'] = [1 if r == '@' else 0 for r in tdf['Away']]
#         #print(tdf.columns)
        tdf['img_URL'] = parsed_img.get('src')
        tdf = tdf.loc[:, ~tdf.columns.duplicated()]
        # print(tdf.columns)

        df.append(tdf)

    except:
        pass
df = pd.concat(df, sort=False)
# [x.replace(",", "").replace(".", "").replace(" ","")
#  for line in file for word in line]
df.to_csv('stats2019_1.csv')
```

    0 
    10 
    20 
    30 
    40 
    50 
    60 
    70 
    80 
    90 
    100 
    110 
    120 
    130 
    140 
    150 
    160 
    170 
    180 
    190 
    200 
    210 
    220 
    230 
    240 
    250 
    260 
    270 
    280 
    290 
    300 
    
    Complete.
    


    ---------------------------------------------------------------------------

    PermissionError                           Traceback (most recent call last)

    <ipython-input-168-ac5737cdd815> in <module>()
        111 # [x.replace(",", "").replace(".", "").replace(" ","")
        112 #  for line in file for word in line]
    --> 113 df.to_csv('stats2019.csv')
        114 
        115 
    

    C:\ProgramData\Anaconda3\lib\site-packages\pandas\core\frame.py in to_csv(self, path_or_buf, sep, na_rep, float_format, columns, header, index, index_label, mode, encoding, compression, quoting, quotechar, line_terminator, chunksize, tupleize_cols, date_format, doublequote, escapechar, decimal)
       1743                                  doublequote=doublequote,
       1744                                  escapechar=escapechar, decimal=decimal)
    -> 1745         formatter.save()
       1746 
       1747         if path_or_buf is None:
    

    C:\ProgramData\Anaconda3\lib\site-packages\pandas\io\formats\csvs.py in save(self)
        134             f, handles = _get_handle(self.path_or_buf, self.mode,
        135                                      encoding=encoding,
    --> 136                                      compression=None)
        137             close = True if self.compression is None else False
        138 
    

    C:\ProgramData\Anaconda3\lib\site-packages\pandas\io\common.py in _get_handle(path_or_buf, mode, encoding, compression, memory_map, is_text)
        398         elif encoding:
        399             # Python 3 and encoding
    --> 400             f = open(path_or_buf, mode, encoding=encoding)
        401         elif is_text:
        402             # Python 3 and no explicit encoding
    

    PermissionError: [Errno 13] Permission denied: 'stats2019.csv'


## Below Code was not used - it was extracting using the YT API. I found a simpler method in further below code snippets


```python
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

DEVELOPER_KEY = "AIzaSyDUeDeyY6TROtz_ANdy_JlmrecjEueIAKk"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def youtube_search(q, max_results=50, order="relevance", token=None, location=None, location_radius=None):

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    search_response = youtube.search().list(
        q=q,
        type="video",
        pageToken=token,
        order=order,
        part="id,snippet",
        maxResults=max_results,
        location=location,
        locationRadius=location_radius

    ).execute()

    videos = []

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append(search_result)
    try:
        nexttok = search_response["nextPageToken"]
        return(nexttok, videos)
    except Exception as e:
        nexttok = "last_page"
        return(nexttok, videos)


def geo_query(video_id):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    video_response = youtube.videos().list(
        id=video_id,
        part='snippet, recordingDetails, statistics'

    ).execute()

    return video_response
```


```python
import sys

#from youtube_videos import youtube_search
import pandas as pd
import json


vid_title = []
vid_id = []

for name in unique_players[0]:

    test = youtube_search(name)
    just_json = test[1]

    video = just_json[0]
    #     print (video['snippet']['title'])
    #     print (video['id']['videoId'])
    player_name = name
    vid_title.append(video['snippet']['title'])
    vid_id.append(video['id']['videoId'])

# token = test[0]
# youtube_search('nfl', token=token)
#res = youtube_search(keyword, token=token)


# def grab_videos(keyword, token=None):
#     res = youtube_search(keyword, token=token)
#     token = res[0]
#     videos = res[1]
#     for vid in range(0,2):
#         video_dict['youID'].append(vid['id']['videoId'])
#         video_dict['title'].append(vid['snippet']['title'])
#         video_dict['pub_date'].append(vid['snippet']['publishedAt'])
#     print ("added " + str(len(videos)) + " videos to a total of " + str(len(video_dict['youID'])))
#     return token


# token = grab_videos("nfl")
# while token != "last_page":
#     token = grab_videos("nfl", token=token)
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-7-55a1ad61a2c0> in <module>()
         12 vid_id=[]
         13 
    ---> 14 for name in unique_players[0]:
         15 
         16     test = youtube_search(name)
    

    NameError: name 'unique_players' is not defined


## This Set of Code first referencs the above code to simply pull player names. I then pull out values from Youtube searches for image URLs


```python
# Full Real Stats

from bs4 import BeautifulSoup
import pandas as pd
import requests
import numpy as np

# set url and year. maxp is # of players to load from table
url = 'https://www.pro-football-reference.com'
year = 2019
maxp = 300

# grab fantasy players. First block grabs urls from table
r = requests.get(url + '/years/' + str(year) + '/fantasy.htm')
soup = BeautifulSoup(r.content, 'html.parser')
parsed_table = soup.find_all('table')[0]

df = []
tdf2 = []
# r_img = requests.get('https://www.pro-football-reference.com/players/M/McCaCh01.htm')
# soup_img = BeautifulSoup(r_img.content, 'html.parser')
# parsed_img= soup_img.find_all('img')[1]
# url= parsed_img.get('src')
# print(url)

# first 2 rows are col headers
for i, row in enumerate(parsed_table.find_all('tr')[2:]):
    if i % 10 == 0:
        print(i, end=' \n')
    if i >= maxp:
        print('\nComplete.')
        break

    try:
        # stub is the piece of URL for each player
        dat = row.find('td', attrs={'data-stat': 'player'})
        name = dat.a.get_text()
        stub = dat.a.get('href')
        stub = stub[:-4] + '/fantasy/' + str(year)
        tdf2.append(name)

    except:
        pass



```

    0 
    10 
    20 
    30 
    40 
    50 
    60 
    70 
    80 
    90 
    100 
    110 
    120 
    130 
    140 
    150 
    160 
    170 
    180 
    190 
    200 
    210 
    220 
    230 
    240 
    250 
    260 
    270 
    280 
    290 
    300 
    
    Complete.
    


    ---------------------------------------------------------------------------

    ValueError                                Traceback (most recent call last)

    <ipython-input-10-808759db188f> in <module>()
         41     except:
         42         pass
    ---> 43 df = pd.concat(df, sort=False)
         44 # [x.replace(",", "").replace(".", "").replace(" ","")
         45 #  for line in file for word in line]
    

    C:\ProgramData\Anaconda3\lib\site-packages\pandas\core\reshape\concat.py in concat(objs, axis, join, join_axes, ignore_index, keys, levels, names, verify_integrity, sort, copy)
        223                        keys=keys, levels=levels, names=names,
        224                        verify_integrity=verify_integrity,
    --> 225                        copy=copy, sort=sort)
        226     return op.get_result()
        227 
    

    C:\ProgramData\Anaconda3\lib\site-packages\pandas\core\reshape\concat.py in __init__(self, objs, axis, join, join_axes, keys, levels, names, ignore_index, verify_integrity, copy, sort)
        257 
        258         if len(objs) == 0:
    --> 259             raise ValueError('No objects to concatenate')
        260 
        261         if keys is None:
    

    ValueError: No objects to concatenate


## This Code pulls out team Logos. I slightly updated the code for players to pull out the image URLs. There is probably a better way - It was broken so I manually added a few to my file (I got Lazy!)


```python
from bs4 import BeautifulSoup
import pandas as pd
import requests
import numpy as np
# grab URL for logos. First block grabs urls from table
r = requests.get('https://teamcolorcodes.com/nfl-team-color-codes')
soup = BeautifulSoup(r.content, 'html.parser')
parsed_table = soup.find_all('p')[2]
maxp = 40
tm_name = []
tm_url = []
img_url = []

for i, row in enumerate(parsed_table.find_all('a')):
    if i % 10 == 0:
        print(i, end=' \n')
    if i >= maxp:
        print('\nComplete.')
        break

    try:

        name = row.get_text()
        stub = row.get('href')
        # print(stub)
        r2 = requests.get(stub)
        soup2 = BeautifulSoup(r2.content, 'html.parser')
        parsed_img = soup2.find_all('p')[5]
        url = parsed_img.a.get('href')
        # print(url)
        tm_name.append(name)
        tm_url.append(stub)
        img_url.append(url)
    except:
        pass
```

    0 
    10 
    20 
    30 
    

## Logic below is to pull out Youtube search info and then extract the video links which I use in the app


```python
import urllib.request
from bs4 import BeautifulSoup


vid_id = []
# vid_id5=[]
for i, name in enumerate(tdf2):
    print(name, ' ', i)
    textToSearch = name+'2019 Highlights +Sports Productions'
    query = urllib.parse.quote(textToSearch)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    # for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
    #      print('https://www.youtube.com' + vid['href'])
    id_url = soup.findAll(attrs={'class': 'yt-uix-tile-link'})[1]
    url_new = id_url['href']
    vid_id.append(url_new)
```

    Christian McCaffrey   0
    Lamar Jackson   1
    Derrick Henry   2
    Aaron Jones   3
    Ezekiel Elliott   4
    Dalvin Cook   5
    Michael Thomas   6
    Travis Kelce   7
    Nick Chubb   8
    Austin Ekeler   9
    Mark Ingram   10
    Dak Prescott   11
    Mark Andrews   12
    Russell Wilson   13
    Chris Godwin   14
    George Kittle   15
    Deshaun Watson   16
    Chris Carson   17
    Darren Waller   18
    Kenny Golladay   19
    Saquon Barkley   20
    Zach Ertz   21
    Joe Mixon   22
    Todd Gurley   23
    Jared Cook   24
    Cooper Kupp   25
    Julio Jones   26
    DeVante Parker   27
    Leonard Fournette   28
    Jameis Winston   29
    Austin Hooper   30
    Amari Cooper   31
    Mike Evans   32
    A.J. Brown   33
    DeAndre Hopkins   34
    Josh Jacobs   35
    Keenan Allen   36
    Miles Sanders   37
    Allen Robinson   38
    Julian Edelman   39
    Alvin Kamara   40
    Marlon Mack   41
    Jarvis Landry   42
    Josh Allen   43
    Tyler Lockett   44
    DJ Chark   45
    Kenyan Drake   46
    Patrick Mahomes   47
    Phillip Lindsay   48
    Kyler Murray   49
    Courtland Sutton   50
    Stefon Diggs   51
    John Brown   52
    Hunter Henry   53
    Michael Gallup   54
    Aaron Rodgers   55
    Tyler Higbee   56
    D.J. Moore   57
    Robert Woods   58
    Carson Wentz   59
    Raheem Mostert   60
    Dallas Goedert   61
    Le'Veon Bell   62
    Mike Gesicki   63
    Calvin Ridley   64
    David Montgomery   65
    Terry McLaurin   66
    Tyler Boyd   67
    Matt Ryan   68
    Deebo Samuel   69
    Marvin Jones   70
    Carlos Hyde   71
    Tyreek Hill   72
    Davante Adams   73
    Sony Michel   74
    Tom Brady   75
    Jason Witten   76
    Michael Burton   77
    Jared Goff   78
    Jimmy Garoppolo   79
    Derek Carr   80
    Kirk Cousins   81
    Ryan Fitzpatrick   82
    Philip Rivers   83
    Baker Mayfield   84
    Gardner Minshew   85
    Drew Brees   86
    Ryan Tannehill   87
    Jacoby Brissett   88
    Daniel Jones   89
    Andy Dalton   90
    Mitchell Trubisky   91
    Sam Darnold   92
    Kyle Allen   93
    Matthew Stafford   94
    Devonta Freeman   95
    Melvin Gordon   96
    Ronald Jones   97
    Adrian Peterson   98
    D.K. Metcalf   99
    James White   100
    Odell Beckham   101
    Emmanuel Sanders   102
    Latavius Murray   103
    Darius Slayton   104
    Jamison Crowder   105
    Devin Singletary   106
    Cole Beasley   107
    Curtis Samuel   108
    Tevin Coleman   109
    James Conner   110
    Mike Williams   111
    Damien Williams   112
    Robby Anderson   113
    Chris Conley   114
    Duke Johnson   115
    Mason Rudolph   116
    Jamaal Williams   117
    David Johnson   118
    Diontae Johnson   119
    Case Keenum   120
    Golden Tate   121
    Larry Fitzgerald   122
    Breshad Perriman   123
    Peyton Barber   124
    Jordan Howard   125
    Tyrell Williams   126
    Marquise Brown   127
    Randall Cobb   128
    Christian Kirk   129
    Royce Freeman   130
    Mecole Hardman   131
    Zach Pascal   132
    LeSean McCoy   133
    Dede Westbrook   134
    Teddy Bridgewater   135
    James Washington   136
    Sammy Watkins   137
    Gus Edwards   138
    DeAndre Washington   139
    Tarik Cohen   140
    Joe Flacco   141
    Will Fuller   142
    Marcus Mariota   143
    Hunter Renfrow   144
    Sterling Shepard   145
    Matt Breida   146
    Adam Thielen   147
    Taysom Hill   148
    Frank Gore   149
    T.Y. Hilton   150
    Kenny Stills   151
    Danny Amendola   152
    Alshon Jeffery   153
    Dwayne Haskins   154
    Brandin Cooks   155
    Darren Fells   156
    Anthony Miller   157
    Steven Sims   158
    Kerryon Johnson   159
    Kyle Rudolph   160
    Rex Burkhead   161
    Nyheim Hines   162
    Tony Pollard   163
    Boston Scott   164
    Corey Davis   165
    Phillip Dorsett   166
    Greg Olsen   167
    Chase Edmonds   168
    Noah Fant   169
    JuJu Smith-Schuster   170
    Jonnu Smith   171
    Jack Doyle   172
    Demarcus Robinson   173
    Kendrick Bourne   174
    Allen Lazard   175
    Drew Lock   176
    Rashaad Penny   177
    John Ross   178
    Evan Engram   179
    Mohamed Sanu   180
    Tyler Eifert   181
    Ryan Griffin   182
    Kareem Hunt   183
    Willie Snead   184
    Jimmy Graham   185
    Auden Tate   186
    Taylor Gabriel   187
    Preston Williams   188
    Alexander Mattison   189
    Marquez Valdes-Scantling   190
    Malcolm Brown   191
    Jeff Driskel   192
    Brian Hill   193
    Jaylen Samuels   194
    Tajae Sharpe   195
    Eric Ebron   196
    Ted Ginn   197
    Nelson Agholor   198
    Cameron Brate   199
    Keelan Cole   200
    Blake Jarwin   201
    Benny Snell   202
    Jordan Akins   203
    David Blough   204
    Eli Manning   205
    Alex Erickson   206
    Gerald Everett   207
    Jacob Hollister   208
    Tre'Quan Smith   209
    Darrel Williams   210
    Allen Hurns   211
    Dawson Knox   212
    Chris Thompson   213
    Will Dissly   214
    Devlin Hodges   215
    Russell Gage   216
    Derrius Guice   217
    O.J. Howard   218
    Adam Humphries   219
    J.D. McKissic   220
    T.J. Hockenson   221
    Demaryius Thomas   222
    Olabisi Johnson   223
    Mike Boone   224
    Josh Gordon   225
    Hayden Hurst   226
    Foster Moreau   227
    Jalen Richard   228
    Jordan Wilkins   229
    Vance McDonald   230
    Albert Wilson   231
    Patrick Laird   232
    Ricky Seals-Jones   233
    Kaden Smith   234
    Nick Boyle   235
    Jeff Wilson   236
    David Moore   237
    Irv Smith Jr.   238
    Brandon Bolden   239
    Justice Hill   240
    Cody Latimer   241
    Matt Moore   242
    Bo Scarbrough   243
    Geronimo Allison   244
    Josh Hill   245
    Dion Lewis   246
    Josh Reynolds   247
    Damiere Byrd   248
    Marcus Johnson   249
    Dare Ogunbowale   250
    Seth Roberts   251
    Kalen Ballage   252
    Giovani Bernard   253
    Miles Boykin   254
    Nick Foles   255
    Ryquell Armstead   256
    Wayne Gallman   257
    Kelvin Harmon   258
    Paul Richardson   259
    DaeSean Hamilton   260
    Ty Johnson   261
    Isaiah McKenzie   262
    Jakobi Meyers   263
    C.J. Uzomah   264
    Demetrius Harris   265
    Jonathan Williams   266
    Tavon Austin   267
    Delanie Walker   268
    Brandon Allen   269
    Marvin Hall   270
    Matt Schaub   271
    Jaron Brown   272
    Vyncint Smith   273
    Greg Ward   274
    Pharoh Cooper   275
    Keke Coutee   276
    Kyle Juszczyk   277
    Malik Turner   278
    Charles Clay   279
    Qadree Ollison   280
    Chester Rogers   281
    Jeremy Sprinkle   282
    Jarius Wright   283
    DeSean Jackson   284
    Jake Kumerow   285
    Scott Miller   286
    Justin Watson   287
    Jakeem Grant   288
    N'Keal Harry   289
    James O'Shaughnessy   290
    

## Here we simply match player name to video link


```python
vid_id2 = []
for i in vid_id:
    vid_id2.append(i[9:])
#vid_id2 = list(dict.fromkeys(vid_id2))
```


```python
unique_name = pd.DataFrame()
unique_name['players'] = tdf2
```


```python
unique_name['id'] = pd.Series(vid_id2)
```


```python
unique_tm = df.Tm.unique()
unique_team = pd.DataFrame()
unique_team['name'] = unique_tm
```
