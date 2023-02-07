import json
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import pandas as pd
import matplotlib.patches as patches
from matplotlib.collections import PatchCollection
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg


def getLineup(team,path):
    '''
    Generate a field visualisation of a lineup between the various replacements.
    
    Parameters:
        team (int): 0 (domicil) or 1 (visitor)
        filename (str) : path to the .json file
        
    Returns: 
        Matplotlib visualisation using the mplsoccer module.
    '''
    
    
    # DESCRIPTION = 'Function' : (x_postion,y_position,x_name,y_name,x_number,y_number,x_nationality,y_nationality,x_cards,y_cards)
    placementOnField = {'Goalkeeper':               (0,39.5,1,40,4,38,8,38,2,36),
                    'Right Center Back':            (18,47.5,19,48,22,46,26,46,20,44),
                    'Left Center Back' :            (18,31.5,19,32,22,30,26,30,20,28),
                    'Center Back' :                 (18,39.5,19,40,22,38,26,38,20,36),
                    'Left Wing Back':               (26,7.5,27,8,30,6,34,6,28,4),
                    'Right Wing Back':              (26,72.5,27,73,30,71,33,71,28,69),
                    'Left Back':                    (22,18.5,23,19,26,17,30,17,24,15),
                    'Right Back':                   (22,61.5,23,62,26,60,30,60,24,58),
                    'Center Defensive Midfield' :   (43,39.5,44,40,47,38,51,38,45,36),
                    'Left Midfield':                (55,12.5,56,13,59,11,63,11,57,9),
                    'Center Midfield':              (58,39.5,59,40,62,38,66,38,60,36),
                    'Center Attacking Midfield':    (75,39.5,76,40,78,38,82,38,76,36),
                    'Right Midfield':               (55,66.5,56,67,59,65,63,65,57,63),
                    'Left Center Midfield':         (60,49.5,61,50,64,48,68,48,62,46),
                    'Left Defensive Midfield':      (45,52.5,46,53,49,51,53,51,47,49),
                    'Right Center Midfield':        (60,29.5,61,30,64,28,68,28,62,26),
                    'Right Defensive Midfield':     (45,27.5,46,28,49,26,53,26,47,24),
                    'Right Attacking Midfield':     (70,27.5,71,28,74,26,78,26,73,24),
                    'Left Attacking Midfield':      (70,52.5,71,53,74,51,78,51,73,49),
                    'Left Wing':                    (90,69.5,91,70,94,68,98,68,92,66),
                    'Right Wing':                   (90,9.5,91,10,94,8,98,8,92,6),
                    'Left Center Forward':          (95,49.5,96,50,99,48,103,48,97,46),
                    'Right Center Forward':         (95,30.5,96,31,99,29,103,29,97,27),
                    'Left Wing Forward':            (92,71.5,93,72,96,70,100,70,94,68),
                    'Right Wing Forward':           (92,9.5,93,9,96,7,100,7,94,5),
                    'Left Forward':                 (95,62.5,96,63,99,61,103,61,97,59),
                    'Right Forward':                (95,18.5,96,18,99,16,103,16,97,14),
                    'Center Forward':               (95,39.5,96,40,99,38,103,38,97,36),
                    'Secondary Striker':            (105,39.5,106,40,109,38,113,38,107,36)}
    
    # Nationality abbreviation
    nationality = {'Austria':'AT', 'Argentina':'AR','Algeria':'DZ',
                   'Belgium':'BE', 'Bulgaria':'BG','Brazil':'BR','Bosnia and Herzegovina':'BA',
                   'Croatia':'HR','Cyprus':'CY','Czech Republic':'SK','Chile':'CL','Colombia':'COL','Cameroon':'CM','Central African Republic':'CF','Costa Rica':'CR','Cape Verde':'CV','Congo, (Kinshasa)':'CG','China':'CHN','Côte d\'Ivoire':'CI','Canada':'CAN',
                   'Denmark':'DK',
                   'Estonia':'EE','Ecuador':'EC',
                   'France':'FR', 'Finland':'FI',
                   'Greece':'EL','Germany':'DE','Ghana':'GHA','Guinea-Bissau':'GW',
                   'Hungary':'HU','Honduras':'HND',
                   'Ireland':'IE','Italy':'IT','Iceland':'ISL',
                   'Japan':'JP',
                   'Korea (South)':'KR',
                   'Latvia':'LV','Luxembourg':'LU', 'Lithuania':'LT',
                   'Morocco':'MAR', 'Monaco':'MCO','Mexico':'MX','Montenegro':'ME','Macedonia, Republic of':'MKD','Mali':'MLI',
                   'Netherlands':'NL','Nigeria':'NGA',
                   'Portugal':'PT','Poland':'PL','Paraguay':'PRY','Peru':'PE',
                   'Romania':'RO','Russia':'RUS',
                   'Spain':'ES','Slovenia':'SI','Sweden':'SE','Slovakia':'SK','Serbia':'RS','Senegal':'SN',
                   'Turkey':'TR','Turkmenistan':'TM','Togo':'TGO',
                   'Uruguay':'UY','United Kingdom':'UK','Uganda':'UG',
                   'Venezuela (Bolivarian Republic)':'VEN'
                    }
    
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
    df_lineups = pd.DataFrame([],columns=['player','position','player_id','number','cards','from','to','nationality','nat_abbr'])
    
    
    # Search for the various instances of the match 
    for players in range(len(lineup_team)):
        for j in range(len(lineup_team[players]['positions'])):
            time_laps.append(lineup_team[players]['positions'][j]['from'])
    
    # Moments of changes
    time_laps = sorted(list(set(time_laps)))
    
    # The 11 titulars 
    for players in range(len(lineup_team)):
        for j in range(len(lineup_team[players]['positions'])):
            if lineup_team[players]['positions'][j]['start_reason'] == "Starting XI":
                df_lineups.loc[line,'player'] = lineup_team[players]['player_name']
                df_lineups.loc[line,'position'] = lineup_team[players]['positions'][j]['position']
                df_lineups.loc[line,'from'] = lineup_team[players]['positions'][j]['from']
                df_lineups.loc[line,'to'] = lineup_team[players]['positions'][j]['to']
                df_lineups.loc[line,'number'] = lineup_team[players]['jersey_number']
                df_lineups.loc[line,'player_id'] = lineup_team[players]['player_id']
                line += 1       
                # Drop the outgoing player
                for i in range(len(df_lineups.index)):
                    if df_lineups['to'][i] != None:
                        continue
                    else:
                        df_lineups['to'][i] = '90:00'


    # Implementation of the dataframes ('df_lineups') of the 11 players on the field and their information      
    for h in range(len(time_laps[1:])):
        for players in range(len(lineup_team)):
            for j in range(len(lineup_team[players]['positions'])):
                if lineup_team[players]['positions'] != [] and lineup_team[players]['positions'][j]['from'] == time_laps[h] and lineup_team[players]['positions'][j]['to'] != time_laps[h]:
                    df_lineups.loc[line,'player'] = lineup_team[players]['player_name']
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
            plt.text(placementOnField[df_lineups.position[d]][2]+0.3,placementOnField[df_lineups.position[d]][3],s=df_lineups['player'][d], fontweight='extra bold')                                       #POSITION

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



getLineup(team=0,path='Lineups_JSON/lineups_69181.json')
