
# coding: utf-8

# # Football Data Scraper
# 
# This was built as a tool to pull out Fantasy and other Stats from the below websites. Code is not perfect, optimized or perfectly annotated - but hopefully is is helpful! The extractions were used to build an interactive Qliksense application.
# * https://www.pro-football-reference.com - This is the main extraction tool
# * https://teamcolorcodes.com/ - This is for color codes and logos
# * https://www.youtube.com/ - This was to pull out video URLS
# 
# 

# In[ ]:


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


# In[ ]:


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


# ## Below Code was not used - it was extracting using the YT API. I found a simpler method in further below code snippets

# In[ ]:


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


# In[ ]:


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


# ## This Set of Code first referencs the above code to simply pull player names. I then pull out values from Youtube searches for image URLs

# In[ ]:


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



# ## This Code pulls out team Logos. I slightly updated the code for players to pull out the image URLs. There is probably a better way - It was broken so I manually added a few to my file (I got Lazy!)

# In[ ]:


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


# ## Logic below is to pull out Youtube search info and then extract the video links which I use in the app

# In[ ]:


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


# ## Here we simply match player name to video link

# In[ ]:


vid_id2 = []
for i in vid_id:
    vid_id2.append(i[9:])
#vid_id2 = list(dict.fromkeys(vid_id2))


# In[ ]:


unique_name = pd.DataFrame()
unique_name['players'] = tdf2


# In[ ]:


unique_name['id'] = pd.Series(vid_id2)


# In[ ]:


unique_tm = df.Tm.unique()
unique_team = pd.DataFrame()
unique_team['name'] = unique_tm

