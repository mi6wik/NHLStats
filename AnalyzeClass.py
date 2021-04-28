## Classes for the shoot analyze program

## Class that will contain methods about either a single player or a group of players 
## when passed data about their shots

import pickle
import os.path
import get_hockey as hockey
import numpy as np
import matplotlib.pyplot as plt
import math
from PIL import Image
from matplotlib.patches import RegularPolygon
import gc

class stats():
    
    
    
    def __init__(self, year, name, team_check=False):
        self.year = year
        self.name = name
        self.team_check = team_check
        
        if self.name == "league":
            self.data = self.get_league_data()
        elif team_check is True:
            self.data = self.get_team_data()
        else:
            self.data = self.get_data()
        
        self.normal = self.normalize()
        self.shot_bin = self.shot_bin()
       
    def retrive_pickle(self):
        #easy way to get the pickle file that is being reference for the object
        self.year = str(self.year)
               #check if data set for that year exists,
               #if not, create it
        path = './'+self.year+'FullDataset.pkl'
        file_test = os.path.exists(path)
          
        if file_test is False:
            hockey.get_data(self.year)
                                
                #open and load the dataset
        with open(path, 'rb') as f:
            game_data = pickle.load(f)
            
        return game_data
        
    def get_data(self):
        gc.disable()        
        self.year = str(self.year)
               #check if data set for that year exists,
               #if not, create it
        path = './'+self.year+'FullDataset.pkl'
        file_test = os.path.exists(path)
          
        if file_test is False:
            hockey.get_data(self.year)
                                
                #open and load the dataset
        with open(path, 'rb') as f:
            game_data = pickle.load(f)
                
        self.data = {}    
        self.data['Shot'] = {}
        self.data['Shot']['x'] = []
        self.data['Shot']['y'] = []
        self.data['Goal'] ={}
        self.data['Goal']['x'] = []
        self.data['Goal']['y'] = []
            
                    
        event_types = ['Shot','Goal']
          
        for data in game_data:
            if 'liveData' not in data:
                continue
                                            
            plays = data['liveData']['plays']['allPlays']
                    
            for play in plays:
                if 'players' in play:
                        for player in play['players']:
                            if player['player']['fullName'] in [self.name] and player['playerType'] in ['Shooter', 'Scorer']:
                                for event in event_types:
                                    if play['result']['event'] in [event]:
                                        if 'x' in play['coordinates']:
                                            self.data[event]['x'].append(play['coordinates']['x'])
                                            self.data[event]['y'].append(play['coordinates']['y'])
        gc.enable()                            
        return self.data    
                        
    def get_team_data(self):
        gc.disable()        
        self.year = str(self.year)
               #check if data set for that year exists,
               #if not, create it
        path = './'+self.year+'FullDataset.pkl'
        file_test = os.path.exists(path)
          
        if file_test is False:
            hockey.get_data(self.year)
                                
                #open and load the dataset
        with open(path, 'rb') as f:
            game_data = pickle.load(f)
                
        self.data = {}    
        self.data['Shot'] = {}
        self.data['Shot']['x'] = []
        self.data['Shot']['y'] = []
        self.data['Goal'] ={}
        self.data['Goal']['x'] = []
        self.data['Goal']['y'] = []
            
                    
        event_types = ['Shot','Goal']
          
        for data in game_data:
            if 'liveData' not in data:
                continue
                                            
            plays = data['liveData']['plays']['allPlays']
                    
            for play in plays:
                if 'players' in play:
                    if play['team']['name'] in [self.name]:
                        for player in play['players']:
                            if player['playerType'] in ['Shooter', 'Scorer']:
                                for event in event_types:
                                    if play['result']['event'] in [event]:
                                        if 'x' in play['coordinates']:
                                            self.data[event]['x'].append(play['coordinates']['x'])
                                            self.data[event]['y'].append(play['coordinates']['y'])
        gc.enable()                            
        return self.data 
                                                       
    def get_league_data(self):
        gc.disable()
        #just like above but specifically for the whole league sans player information        
        self.year = str(self.year)
               #check if data set for that year exists,
               #if not, create it
        path = './'+self.year+'FullDataset.pkl'
        file_test = os.path.exists(path)
          
        if file_test is False:
            hockey.get_data(self.year)
                                
                #open and load the dataset
        with open(path, 'rb') as f:
            game_data = pickle.load(f)
                
        self.data = {}    
        self.data['Shot'] = {}
        self.data['Shot']['x'] = []
        self.data['Shot']['y'] = []
        self.data['Goal'] ={}
        self.data['Goal']['x'] = []
        self.data['Goal']['y'] = []
                              
        event_types = ['Shot','Goal']
          
        for data in game_data:
            if 'liveData' not in data:
                continue
                                            
            plays = data['liveData']['plays']['allPlays']
                    
            for play in plays:
                for event in event_types:
                    if play['result']['event'] in [event]:
                        if 'x'in play['coordinates']:
                            self.data[event]['x'].append(play['coordinates']['x'])
                            self.data[event]['y'].append(play['coordinates']['y'])
        gc.enable()                             
        return self.data                 
            
        
    def normalize(self):
        gc.disable()
        #normalize the data for better data analysis           
        goalx = self.data['Goal']['x']
        goaly = self.data['Goal']['y']
        
        self.all_shots_x = self.data['Shot']['x'] + goalx
        self.all_shots_y = self.data['Shot']['y'] + goaly
                
        self.x_shots_norm = []
        self.y_shots_norm = []
        self.x_goals_norm = []
        self.y_goals_norm = []
        
        for i,s in enumerate(self.all_shots_x):
            if self.all_shots_x[i] < 0:
                self.x_shots_norm.append(-self.all_shots_x[i])
                self.y_shots_norm.append(-self.all_shots_y[i])
            else:
                self.x_shots_norm.append(self.all_shots_x[i])
                self.y_shots_norm.append(self.all_shots_y[i])
                
        for i,s in enumerate(goalx):
            if goalx[i] < 0:
                self.x_goals_norm.append(-goalx[i])
                self.y_goals_norm.append(-goaly[i])
            else:
                self.x_goals_norm.append(goalx[i])
                self.y_goals_norm.append(goaly[i])
                
        return [self.x_shots_norm,
                self.y_shots_norm,
                self.x_goals_norm,
                self.y_goals_norm]
        gc.enable()
        
    def shot_bin(self):    
        gc.disable()
        #bin the shots for graphing or just to have
        xbnds = np.array([-100, 100])
        ybnds = np.array([-100, 100])
        extent = [xbnds[0],xbnds[1], ybnds[0],xbnds[1]]
        gridsize = 30
        mincnt = 0
        
        player_hex_data = plt.hexbin(self.all_shots_x, self.all_shots_y, gridsize=gridsize,\
                                     extent=extent,mincnt=mincnt,alpha=0.0,visible=False)
        player_goal_hex_data = plt.hexbin(self.x_goals_norm, self.y_goals_norm, gridsize=gridsize,\
                                          extent=extent,mincnt=mincnt,alpha=0.0,visible=False)
        plt.close()
        
        self.player_verts = player_hex_data.get_offsets()
        self.player_shot_frequency = player_hex_data.get_array()
        self.player_goal_frequency = player_goal_hex_data.get_array()
        gc.enable()
        return [self.player_verts,
                self.player_shot_frequency,
                self.player_goal_frequency]
    
    
    def plot(self):
        #shows the players shots on goal on one chart and 
        #actual goals made on another.
        gc.disable()
        fig, ax = plt.subplots(2)
        k = 0
        for a in ax:
            ax[k].set_facecolor('white')                          
         #remove axis labeling
            ax[k].set_xticklabels(labels=[''],fontsize=18, alpha=.7,minor=False)
            ax[k].set_yticklabels(labels=[''],fontsize=18, alpha=.7,minor=False)
            
            I = Image.open('./hockeyhalf.png')
            ax[k].imshow(I);width, height = I.size
            k = k + 1
            
        
        fig.patch.set_facecolor("white")
        fig.patch.set_alpha(0.0) 
    # Calculate the scaling factor and offset (trial and error)
        scalingx=width/100-0.6    
        scalingy=height/100+.5;
        x_trans=33;
        y_trans=height/2
        
    # We will want to scale the size of our hex bins with the image so we calculate a "radius" scaling factor here
        S = 3.8*scalingx
   
        for i,v in enumerate(self.player_verts):
        
        #ignore empties
            if self.player_shot_frequency[i] < 1:
                continue
            scaled_player_shot_frequency = self.player_shot_frequency[i]/max(self.player_shot_frequency)
            scaled_player_goal_frequency = self.player_goal_frequency[i]/max(self.player_goal_frequency)
        
            s_radius = S*math.sqrt(scaled_player_shot_frequency)
            g_radius = S*math.sqrt(scaled_player_goal_frequency)
            
            s_hex = RegularPolygon((x_trans+v[0]*scalingx,y_trans-v[1]*scalingy), numVertices=6,radius=s_radius,orientation=np.radians(0),alpha=0.5,edgecolor=None,color="blue")
            g_hex = RegularPolygon((x_trans+v[0]*scalingx,y_trans-v[1]*scalingy), numVertices=6,radius=g_radius,orientation=np.radians(0),alpha=0.5,edgecolor=None,color="red")
        
            ax[0].add_patch(s_hex)
            ax[1].add_patch(g_hex)    
        gc.enable()    
        plt.show()
        
def plot_compare(instances):
    #compares anyone to anyone. including the league.
    #instances needs to be a _D array in the arrangement you want the graphs to be
    nrows = len(instances)
    ncols = len(instances[0])
    
    I = Image.open('./hockeyhalf.png')
    width, height = I.size
    
    fig, ax = plt.subplots(nrows=nrows,ncols=ncols)

    for i in range(0, nrows):        
        for j in range(0, ncols):
            ax[i,j].set_facecolor('white')
            #ax[i].set_xticklabels(labels=[''],fontsize=18, alpha=.7,minor=False)
            #ax[i].set_yticklabels(labels=[''],fontsize=18, alpha=.7,minor=False)
            ax[i,j].xaxis.set_major_formatter(plt.NullFormatter())
            ax[i,j].yaxis.set_major_formatter(plt.NullFormatter())
            
            ax[i,j].tick_params(axis='x',which='both',bottom=False,top=False,labelbottom=False)
            ax[i,j].tick_params(axis='y',which='both',left=False,right=False,labelright=False)
          
            ax[i,j].imshow(I)      
    
    fig.patch.set_facecolor("white")
    fig.patch.set_alpha(0.0) 
    # Calculate the scaling factor and offset (trial and error)
    scalingx=width/100-0.6    
    scalingy=height/100+.5
    x_trans=33
    y_trans=height/2
        
    # We will want to scale the size of our hex bins with the image so we calculate a "radius" scaling factor here
    S = 3.8*scalingx

    for p in range(0,nrows):
        for q in range(0,ncols):
            w = instances[p][q]
            ax[p,q].title.set_text(" "+w.name+" "+w.year+" ")         
            for k,v in enumerate(w.player_verts):
                if w.player_shot_frequency[k] < 1:
                    continue
                scaled_player_shot_frequency = w.player_shot_frequency[k]/max(w.player_shot_frequency)
                scaled_player_goal_frequency = w.player_goal_frequency[k]/max(w.player_goal_frequency)
                
                s_radius = S*math.sqrt(scaled_player_shot_frequency)
                g_radius = S*math.sqrt(scaled_player_goal_frequency)
                    
                s_hex = RegularPolygon((x_trans+v[0]*scalingx,y_trans-v[1]*scalingy),\
                                       numVertices=6,radius=s_radius,orientation=np.radians(0),alpha=0.5,edgecolor=None,color="blue")
                g_hex = RegularPolygon((x_trans+v[0]*scalingx,y_trans-v[1]*scalingy), \
                                       numVertices=6,radius=g_radius,orientation=np.radians(0),alpha=0.5,edgecolor=None,color="red")
                
                ax[p,q].add_patch(s_hex)
                ax[p,q].add_patch(g_hex)
        
    plt.show()
