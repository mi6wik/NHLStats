# -*- coding: utf-8 -*-
import requests
import pickle

def get_data(year):
# Set up API Call Variables
    game_data = []
    season_type = '02' #regular season
    max_game_ID = 1300 #game events in the year

# Loop over the counder and format the API call
    for i in range(0,max_game_ID):
        pk = str(year+season_type+str(i).zfill(4))
        r = requests.get(url='http://statsapi.web.nhl.com/api/v1/game/'
                         +pk+'/feed/live')
        p = (i/max_game_ID)*100
        if (p%1) == 0:
            print(p)
        
        data = r.json()
        print(i)
        if 'messageNumber' in data or len(data['gameData']['players']) < 1:
                print('no data for '+pk)
                continue
        
        game_data.append(data)  
        print(data['gameData']['datetime']['dateTime']+"  "+data['gameData']['teams']['away']['abbreviation']  \
              +"  @  "+data['gameData']['teams']['home']['abbreviation'])
            
    with open('./'+year+'FullDataset.pkl', 'wb') as f:
        pickle.dump(game_data, f, pickle.HIGHEST_PROTOCOL)

    
def get_latest(year):
    """opens up pickle file from 'year' and makes sure that it is up to date."""
    
    game_data = []
    season_type = '02' #regular season
    max_game_ID = 1300 #game events in the year
    
    with open('./'+year+'FullDataset.pkl', 'rb') as f:
        game_data = pickle.load(f)
        
    #set up a list of game ids that we already have and compare them to what we
    #still need    
    got_list = []
    for i in range(0, len(game_data)):
        got_list.append(str(game_data[i]['gameData']['game']['pk']))
    
    need_list = []
    for j in range(1,max_game_ID):
        need_list.append(year+season_type+str(j).zfill(4))
    
    need_list = list(set(need_list).difference(got_list))    
    
    #retrive needed data from the api and append it to the pickle file.
    for pk in need_list:
        r = requests.get(url='http://statsapi.web.nhl.com/api/v1/game/'+pk+'/feed/live')        
        data = r.json()
               
        if 'messageNumber' in data or len(data['gameData']['players']) < 1:
                print('no data for '+pk)
                continue
            
        game_data.append(data)    
        print(data['gameData']['datetime']['dateTime']+"  "+data['gameData']['teams']['away']['abbreviation']  \
              +"  @  "+data['gameData']['teams']['home']['abbreviation'])
        
    with open('./'+year+'FullDataset.pkl', 'wb') as f:
        pickle.dump(game_data, f, pickle.HIGHEST_PROTOCOL)

def get_teams(year):
    team_list = []
    



