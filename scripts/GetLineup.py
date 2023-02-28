import json
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import pandas as pd
import matplotlib.patches as patches
from matplotlib.collections import PatchCollection
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
from MPL_utils import get_placements, get_nationalities


def getLineup(team,path):
    '''
    Generate a field visualisation of a lineup between the various replacements.
    
    Parameters:
        team (int): 0 (domicil) or 1 (visitor)
        filename (str) : path to the .json file
        
    Returns: 
        Matplotlib visualisation using the mplsoccer module.
    '''
    
    
    # 'Function' : (x_postion,y_position,x_name,y_name,x_number,y_number,x_nationality,y_nationality,x_cards,y_cards)
    placementOnField = get_placements()
    
    # Nationality abbreviation
    nationality = get_nationalities()
    
    color_team = 'blue' if team == 0 else 'red'
    
    # OPEN THE FILE
    with open(f'{path}') as file:
        data = json.load(file)
    
    # TEAM NAME
    domicil_team = data[0]['team_name']
    visitor_team = data[1]['team_name']
    
    
    # Run domicil or visitor team 
    lineup_team = data[team]['lineup']


    # Course the moments of the match 
    line = 0
    time_laps = ['90:00']
    
    # Dataframes of the lineups on the field
    df_lineups = pd.DataFrame([],columns=['player','nickname','position','player_id','number','cards','from','to','nationality','nat_abbr'])
    
    
    # Search for the various instances of the match 
    for players in range(len(lineup_team)):
        for j in range(len(lineup_team[players]['positions'])):
            print(lineup_team[players]['positions'][j]['from'])
            time_laps.append(lineup_team[players]['positions'][j]['from'])
    
    # Moments of changes
    time_laps = sorted(list(set(time_laps)))
    print(time_laps)
    
    
    # The 11 titulars 
    for players in range(len(lineup_team)):
        for j in range(len(lineup_team[players]['positions'])):
            if lineup_team[players]['positions'][j]['start_reason'] == "Starting XI":
                df_lineups.loc[line,'player'] = lineup_team[players]['player_name']
                df_lineups.loc[line,'nickname'] = lineup_team[players]['player_nickname']
                df_lineups.loc[line,'position'] = lineup_team[players]['positions'][j]['position']
                df_lineups.loc[line,'from'] = lineup_team[players]['positions'][j]['from']
                df_lineups.loc[line,'to'] = lineup_team[players]['positions'][j]['to']
                df_lineups.loc[line,'number'] = lineup_team[players]['jersey_number']
                df_lineups.loc[line,'player_id'] = lineup_team[players]['player_id']
                line += 1       
                # Drop the outgoing player
                df_lineups.to.replace({None:'90:00'})
    print(df_lineups)

    # Implementation of the dataframes ('df_lineups') of the 11 players on the field and their information      
    for h in range(len(time_laps[1:])):
        for players in range(len(lineup_team)):
            for j in range(len(lineup_team[players]['positions'])):
                if lineup_team[players]['positions'] != [] and lineup_team[players]['positions'][j]['from'] == time_laps[h] and lineup_team[players]['positions'][j]['to'] != time_laps[h]:
                    df_lineups.loc[line,'player'] = lineup_team[players]['player_name']
                    df_lineups.loc[line,'nickname'] = lineup_team[players]['player_nickname']
                    df_lineups.loc[line,'position'] = lineup_team[players]['positions'][j]['position']
                    df_lineups.loc[line,'from'] = lineup_team[players]['positions'][j]['from']
                    df_lineups.loc[line,'nationality'] = lineup_team[players]['country']['name']
                    df_lineups.loc[line,'number'] = lineup_team[players]['jersey_number']
                    df_lineups.loc[line,'player_id'] = lineup_team[players]['player_id']
            
                    if lineup_team[players]['positions'][j]['to'] != None:
                        df_lineups.loc[line,'to'] = lineup_team[players]['positions'][j]['to']
                    else:
                        df_lineups.loc[line,'to'] = '90:00'
                    line += 1
            
            # CARDS
            if len(lineup_team[players]['cards']) > 0:
                df_lineups.loc[line,'cards'] = str(lineup_team[players]['cards'][-1]['card_type'])
            else:
                None
            
                
        # Drop the tactical shift of a player
        df_lineups.drop_duplicates(subset='player', keep='last', inplace=True, ignore_index=True)
    
        # Drop the outgoing player and reset index of the dataframe
        df_lineups = df_lineups[(df_lineups.to != time_laps[h])]
        df_lineups = df_lineups[:11].reset_index(drop=True)    
        
        # NATIONALITY
        for k in range(len(df_lineups.nationality)):
            for cle,value in nationality.items(): 
                if df_lineups.nationality[k] == cle:
                    df_lineups.nat_abbr[k] = value
        
        print(df_lineups)
        # VISUALISATION
        pitch= Pitch(pitch_color='grass', line_color='white')
        fig, ax = pitch.draw()
        fig.set_size_inches(10,7)
        RCards = []
        YCards = []
        for d in range(len(df_lineups.index)):            
            plt.scatter(placementOnField[df_lineups.position[d]][0],placementOnField[df_lineups.position[d]][1], c=color_team, marker='p', s=100)
            plt.scatter(placementOnField[df_lineups.position[d]][0],placementOnField[df_lineups.position[d]][1]-1, c='black')
            plt.text(placementOnField[df_lineups.position[d]][4],placementOnField[df_lineups.position[d]][5],s=df_lineups['number'][d], fontweight='extra bold', fontsize=15, c='cyan')                #NUMBER   
            if df_lineups['nickname'][d] != None :
                plt.text(placementOnField[df_lineups.position[d]][2]+0.3,placementOnField[df_lineups.position[d]][3],s=df_lineups['nickname'][d], fontweight='extra bold')                                     #POSITION
            else:
                plt.text(placementOnField[df_lineups.position[d]][2]+0.3,placementOnField[df_lineups.position[d]][3],s=df_lineups['player'][d], fontweight='extra bold')                                     #POSITION

            # Add nationality flag
            for i in range(len(df_lineups.nationality)):
                if df_lineups.nationality[i] == 'Guadeloupe':
                    df_lineups.nationality[i] = 'France'
                elif df_lineups.nationality[i] == 'Korea (South)':
                    df_lineups.nationality[i] = 'South Korea'
                elif df_lineups.nationality[i] == 'Macedonia, Republic of':
                    df_lineups.nationality[i] = 'Macedonia'
                elif df_lineups.nationality[i] == 'Wales':
                    df_lineups.nationality[i] = 'United Kingdom'
                    
            
            flag = mpimg.imread(f'pictures/flag/{df_lineups.nationality[d]}.png')
            imagebox_away = OffsetImage(flag, zoom=0.16)
            aa = AnnotationBbox(imagebox_away, (placementOnField[df_lineups.position[d]][6]+2.5, placementOnField[df_lineups.position[d]][7]-1.2), frameon=False)
            ax.add_artist(aa)
            
            #
            if df_lineups['cards'][d] == 'Yellow Card':

                YCards.append(patches.Rectangle((placementOnField[df_lineups.position[d]][8],placementOnField[df_lineups.position[d]][9]),1.5,2))
            elif df_lineups['cards'][d] == 'Red Card':
                RCards.append(patches.Rectangle((placementOnField[df_lineups.position[d]][8],placementOnField[df_lineups.position[d]][9]),1.5,2))
            else:
                continue
        pcY = PatchCollection(YCards,linewidth=1, edgecolor='k', facecolor='y')
        pcR = PatchCollection(RCards,linewidth=1, edgecolor='k', facecolor='r')
        
        
        ax.add_collection(pcY)   
        ax.add_collection(pcR)  
         
        plt.subplots_adjust(right=1, top=1, bottom=0, left=0)
        plt.suptitle(f'{time_laps[h]} to {time_laps[h+1]}', fontweight='extra bold')
        plt.text(30,-1,f'{domicil_team}', fontweight='bold', color='blue', fontsize=15)
        plt.text(58,-1, 'VS', fontweight='bold', color='white', fontsize=15)
        plt.text(75,-1, f'{visitor_team}', fontweight='bold', color='red', fontsize=15)
        plt.show()
    



getLineup(team=1,path='Lineups_JSON/lineups_15946.json')
