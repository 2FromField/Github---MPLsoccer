import json
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import pandas as pd
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
from MPL_utils import get_nationalities, get_placements


def Evolving_both_Lineups(path):
    """ Evolving display of the two teams compositions throughout the match 

    Args:
        path (_path_): path to the .json file

    Returns:
        Matplotlib visualisation using the mplsoccer module
    """

    # 'Function' : (x_postion,y_position,x_name,y_name,x_number,y_number,x_nationality,y_nationality,x_cards,y_cards)
    placementOnField = get_placements()
    # Nationality abbreviation from the full name
    nationality = get_nationalities()


    # OPEN THE FILE
    with open(f'{path}') as file:
        data = json.load(file)


    # Team name
    domicil_team_name = data[0]['team_name']
    visitor_team_name = data[1]['team_name']

    # Run domicil or visitor team lineups
    lineup_home_team = data[0]['lineup']
    lineup_away_team = data[1]['lineup']

    # Course the moments of the match 
    home_time_laps = ['90:00']
    away_time_laps = ['90:00']


    # Get the moments of changes
    for home,away in zip(range(len(lineup_home_team)),range(len(lineup_away_team))):
        for j in range(len(lineup_home_team[home]['positions'])):
            home_time_laps.append(lineup_home_team[home]['positions'][j]['from'])
        for p in range(len(lineup_away_team[away]['positions'])):
            away_time_laps.append(lineup_away_team[away]['positions'][p]['from'])  
    
    home_time_laps = sorted(list(set(home_time_laps)))
    away_time_laps = sorted(list(set(away_time_laps)))
    time_laps = sorted(set(home_time_laps + away_time_laps))
    
    
    # Create both team's dataframe with all the players and their information at the different positions furing the match
    def get_df_event(lineup):
        df_lineups = pd.DataFrame([],columns=['player','nickname','position','player_id','number','from','to','nationality','nat_abbr'])
        line = 0
        
        for players in range(len(lineup)):
            for p in range(len(lineup[players]['positions'])):
                df_lineups.loc[line,'player'] = lineup[players]['player_name']
                df_lineups.loc[line,'nickname'] = lineup[players]['player_nickname']
                df_lineups.loc[line,'position'] = lineup[players]['positions'][p]['position']
                df_lineups.loc[line,'from'] = lineup[players]['positions'][p]['from']
                df_lineups.loc[line,'to'] = lineup[players]['positions'][p]['to']
                df_lineups.loc[line,'nationality'] = lineup[players]['country']['name']
                df_lineups.loc[line,'number'] = lineup[players]['jersey_number']
                df_lineups.loc[line,'player_id'] = lineup[players]['player_id']
                line += 1

        df_lineups.to = df_lineups.to.replace({None:'90:00'})
        
        return df_lineups
    
    
    df_lineups_home = get_df_event(lineup_home_team)
    df_lineups_away = get_df_event(lineup_away_team)
    
    
    # add the NATIONALITY to the dataframe
    for k,m in zip(range(len(df_lineups_home.nationality)),range(len(df_lineups_away.nationality))):
        for cle,value in nationality.items(): 
            if df_lineups_home.nationality[k] == cle:
                df_lineups_home.nat_abbr[k] = value
            if df_lineups_away.nationality[m] == cle:
                df_lineups_away.nat_abbr[m] = value
    
    
    # Lineups per moments of changes 
    for j in range(len(time_laps)-1):
        df_away = df_lineups_away[(df_lineups_away['to'] >= time_laps[j+1]) & (df_lineups_away['from'] < time_laps[j+1])].reset_index(drop=True)
        df_home = df_lineups_home[(df_lineups_home['to'] >= time_laps[j+1]) & (df_lineups_home['from'] < time_laps[j+1])].reset_index(drop=True)

  
  
        # VISUALISATION
        fig, axs = plt.subplots(nrows=2, figsize=(7, 7.5))
        fig.set_facecolor('black')
        
        
        # 1st pitch
        pitch = Pitch(goal_type='box', goal_alpha=.5, pitch_color='#aabb97', line_color='white',
                    stripe_color='#c2d59d', stripe=True, linewidth=1)  # you can also adjust the transparency (alpha)

        for d in range(len(df_home.index)):            
            pitch.scatter(placementOnField[df_home.position[d]][0],placementOnField[df_home.position[d]][1], c='blue', marker='p', s=100, ax=axs[0])
            pitch.scatter(placementOnField[df_home.position[d]][0],placementOnField[df_home.position[d]][1]-1, c='black', ax=axs[0])
            axs[0].text(placementOnField[df_home.position[d]][4]-1,placementOnField[df_home.position[d]][5],s=df_home['number'][d], fontweight='extra bold', fontsize=10, c='cyan')                #NUMBER   
            if df_home['nickname'][d] != None :
                axs[0].text(placementOnField[df_home.position[d]][2]+1,placementOnField[df_home.position[d]][3]+1,s=df_home['nickname'][d], fontweight='extra bold', fontsize=7)                                     #POSITION
            else:
                axs[0].text(placementOnField[df_home.position[d]][2]+1,placementOnField[df_home.position[d]][3]+1,s=df_home['player'][d], fontweight='extra bold', fontsize=7)                                     #POSITION

            # Add nationality flag of each player
            for i in range(len(df_home.nationality)):
                if df_home.nationality[i] == 'Guadeloupe':
                    df_home.nationality[i] = 'France'
                elif df_home.nationality[i] == 'Korea (South)':
                    df_home.nationality[i] = 'South Korea'
                elif df_home.nationality[i] == 'Macedonia, Republic of':
                    df_home.nationality[i] = 'Macedonia'
                elif df_home.nationality[i] == 'Wales':
                    df_home.nationality[i] = 'United Kingdom'
                    
            flag = mpimg.imread(f'pictures/flag/{df_home.nationality[d]}.png')
            imagebox_away = OffsetImage(flag, zoom=0.10)
            aa_home = AnnotationBbox(imagebox_away, (placementOnField[df_home.position[d]][6]+2.5, placementOnField[df_home.position[d]][7]-1.2), frameon=False)
            axs[0].add_artist(aa_home)
        
        pitch.draw(axs[0])
            
            
        # 2nd pitch
        pitch = Pitch(goal_type='line', pitch_color='#aabb97', line_color='white',
                    stripe_color='#c2d59d', stripe=True, linewidth=1)
    
        for d in range(len(df_away.index)):            
            pitch.scatter((120-placementOnField[df_away.position[d]][0]),(80-placementOnField[df_away.position[d]][1]), c='red', marker='p', s=100, ax=axs[1])
            pitch.scatter((120-placementOnField[df_away.position[d]][0]),(80-placementOnField[df_away.position[d]][1]-1), c='black', ax=axs[1])
            axs[1].text((112-placementOnField[df_away.position[d]][4]-1),(80-placementOnField[df_away.position[d]][5]),s=df_away['number'][d], fontweight='extra bold', fontsize=10, c='cyan')                #NUMBER   
            if df_away['nickname'][d] != None :
                axs[1].text((105-placementOnField[df_away.position[d]][2]+1),(80-placementOnField[df_away.position[d]][3]+5),s=df_away['nickname'][d], fontweight='extra bold', fontsize=7)                                     #POSITION
            else:
                axs[1].text((105-placementOnField[df_away.position[d]][2]+1),(80-placementOnField[df_away.position[d]][3]+5),s=df_away['player'][d], fontweight='extra bold', fontsize=7)                                     #POSITION

            # Add nationality flag of each player
            for i in range(len(df_away.nationality)):
                if df_away.nationality[i] == 'Guadeloupe':
                    df_away.nationality[i] = 'France'
                elif df_away.nationality[i] == 'Korea (South)':
                    df_away.nationality[i] = 'South Korea'
                elif df_away.nationality[i] == 'Macedonia, Republic of':
                    df_away.nationality[i] = 'Macedonia'
                elif df_away.nationality[i] == 'Wales':
                    df_away.nationality[i] = 'United Kingdom'
                    
            flag = mpimg.imread(f'pictures/flag/{df_away.nationality[d]}.png')
            imagebox_away = OffsetImage(flag, zoom=0.10)
            aa_away = AnnotationBbox(imagebox_away, ((120-placementOnField[df_away.position[d]][6]+2.5),(80-placementOnField[df_away.position[d]][7]-1.2)), frameon=False)
            axs[1].add_artist(aa_away)
        
        pitch.draw(axs[1])

        # MIDDLE TEXT
        plt.text(45,-7, f'{time_laps[j]} to {time_laps[j+1]}', fontweight='extra bold', color='white')
        plt.text(20,-15,f'{domicil_team_name}', fontweight='bold', color='blue', fontsize=15)
        plt.text(58,-15, 'VS', fontweight='bold', color='white', fontsize=15)
        plt.text(75,-15, f'{visitor_team_name}', fontweight='bold', color='red', fontsize=15)

        # Parameters
        plt.subplots_adjust(left=0,right=1,bottom=0,top=1)
        plt.show()


Evolving_both_Lineups('Lineups_JSON/lineups_15973.json')