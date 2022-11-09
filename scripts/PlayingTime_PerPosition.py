import json
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import pandas as pd
import numpy as np
import glob

def GetPlayingTimePerPosition(path):
    '''
    Generate a dataframe containing all th eplayers retrieved from the files and their respective playing time according to their position on the field
    
    Parameters:
        path (str) : path to the .json file(s)
        
    Returns: 
        Visualisation of the dataframe 
        The Dataframe
    '''

    df_all_players = pd.DataFrame([],columns=['player','position','from','to','playing_time','team'])

    # Browse all files 
    for filename in glob.glob(path):
        
        # OPEN THE FILE
        with open(f'{filename}') as file:
            data = json.load(file)

        # DOMCIL / VISITOR
        for team in range(len(data)):
            team_name = data[team]['team_name']
            
            # Dataframes of the lineups on the field
            line = 0
            df_match = pd.DataFrame([],columns=['player','position','from','to','playing_time','team'])
            
            # Implementation of the dataframes ('df_lineups') of the 11 players on the field and their information      
            for players in range(len(data[team]['lineup'])):
                
                for j in range(len(data[team]['lineup'][players]['positions'])):
                    df_match.loc[line,'team'] = team_name
                    df_match.loc[line,'player'] = data[team]['lineup'][players]['player_name']
                    df_match.loc[line,'position'] = data[team]['lineup'][players]['positions'][j]['position']
                    df_match.loc[line,'from'] = data[team]['lineup'][players]['positions'][j]['from']
                    if data[team]['lineup'][players]['positions'][j]['to'] != None:
                        df_match.loc[line,'to'] = data[team]['lineup'][players]['positions'][j]['to']
                    else:
                        df_match.loc[line,'to'] = '90:00'
                    #
                    line += 1
        
            # Function to obtain the playing time at a position
            def getPlayingTime(df,entrance,exit):
                '''
                Calculating the playing time at a player's position from a 'mm:ss' format
                        
                Parameters:
                    entrance (str) : '85:44' (example)
                    exit (str) : '90:00' (example)
                    
                Returns: 
                    Return the playing time at a player's position in the format: 'mm:ss'
                '''
                # SECONDS
                if int(entrance[3:]) == 0 and int(exit[3:]) == 0:
                    seconds = 0
                    # MINUTES
                    if int(entrance[3:]) == 0:
                        minutes = int(exit[:2])-int(entrance[:2])
                    else:
                        minutes = (int(exit[:2])-int(entrance[:2]))
                #
                elif int(entrance[:2]) != int(exit[:2]):
                    if int(entrance[3:]) == 0:
                        seconds = int(exit[3:]) + (int(entrance[3:]))
                    else:
                        seconds = int(exit[3:]) + (60-int(entrance[3:]))
                    # MINUTES
                    if int(entrance[3:]) == 0:
                        minutes = int(exit[:2])-int(entrance[:2])
                    else:
                        minutes = (int(exit[:2])-int(entrance[:2]))-1
                #        
                else:
                    seconds = int(exit[3:]) - int(entrance[3:])
                    # MINUTES
                    if int(entrance[3:]) == 0:
                        minutes = int(exit[:2])-int(entrance[:2])
                    else:
                        minutes = (int(exit[:2])-int(entrance[:2]))
                
                # SECONDS > 60 -> +1 minute
                if seconds > 59:
                    minutes += 1
                    seconds = seconds - 60   
                
                # Add 0 if len(minutes or seconds) == 1
                if len(str(minutes)) == 1:
                    minutes = f'0{minutes}'
                if len(str(seconds)) == 1:
                    seconds = f'0{seconds}'
                    
                # RETURN
                return f'{minutes}:{seconds}'
            
            # USE of the previous function
            line_playing_time = 0
            for i in range(len(df_match.index)):
                df_match.loc[line_playing_time,'playing_time'] = getPlayingTime(df_match,df_match['from'][i],df_match['to'][i])
                #
                line_playing_time += 1


            ## Implementation of the database of all players of all teams
            if len(df_all_players) == 0:
                # Initilisation of the dataframe
                df_all_players = df_match
                
            elif len(df_all_players) > 1:
                for i in range(len(df_match.index)):
                    # Calculation of the average playing_time at a position
                    if len(df_all_players[(df_all_players.player == df_match.player[i]) & (df_all_players.position == df_match.position[i])]) > 0:
                        filter = df_all_players[(df_all_players.player == df_match.player[i]) & (df_all_players.position == df_match.position[i])]
                        mins = int(np.mean([int(df_all_players.playing_time[filter.index[0]][:2]),int(df_match.playing_time[i][:2])]))
                        secs = int(np.mean([int(df_all_players.playing_time[filter.index[0]][3:]),int(df_match.playing_time[i][3:])]))
                        
                        # Add 0 if len(minutes or seconds) == 1
                        if len(str(mins)) == 1:
                            mins = f'0{mins}'
                        if len(str(secs)) == 1:
                            secs = f'0{secs}'
                            
                        df_all_players.playing_time[filter.index[0]] = f'{mins}:{secs}'
                    
                    else:
                        # Add the new player 
                        df_all_players.loc[len(df_all_players)] = df_match.loc[i]


    # to_droped = Number of duplicates
    to_droped = 0
    for i in range(len(df_all_players.index)):
        if len(df_all_players[(df_all_players.player == df_all_players.player[i]) & (df_all_players.position == df_all_players.position[i])]) > 1:
            to_droped += len(df_all_players[(df_all_players.player == df_all_players.player[i]) & (df_all_players.position == df_all_players.position[i])])-1

    # Addition of new players not in the database and calculation of the average playing time of the others
    for i in range(len(df_all_players.index)-to_droped):
        if len(df_all_players[(df_all_players.player == df_all_players.player[i]) & (df_all_players.position == df_all_players.position[i])]) > 1:
            df_all_players = df_all_players.drop(df_all_players[(df_all_players.player == df_all_players.player[i]) & (df_all_players.position == df_all_players.position[i])].index[1])
            df_all_players = df_all_players.reset_index(drop=True)

    # Filtering, sorting, and removing unecessary columns
    df_all_players = df_all_players.sort_values(by=['team'])
    df_all_players = df_all_players.reset_index(drop=True)
    df_all_players = df_all_players.drop(['from','to'],axis=1)

    print(df_all_players)
    return df_all_players    


GetPlayingTimePerPosition(path='Lineups_JSON/*.json')

