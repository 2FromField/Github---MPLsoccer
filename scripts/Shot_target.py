import pandas as pd
import glob
import statsbomb as sb
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def Shot_target(pathfile, team_name, player_name=None):
    """ Visualisation of a team's shooting zones (or player's shooting zone)

    Args:
        pathfile (str): path to the files
        team_name (str): name of the team
    """

    line = 0
    dataset = pd.DataFrame([], columns=['x','y','target','outcome','color'])

    for filename in glob.glob(pathfile):
        event_id = filename[21:26]
        events = sb.Events(event_id = f'{event_id}')
        df = events.get_dataframe(event_type = 'shot')
        
        df_ingoal = df[(df.team == team_name) & (df.outcome == 'Goal')].reset_index(drop=True)
        df_saved = df[(df.team == team_name) & (df.outcome == 'Saved')].reset_index(drop=True)
        df_goal = df_ingoal.append(df_saved).reset_index(drop=True)
        
        # New dataframe with only shots on target (dataset)
        for i in range(len(df_goal.index)):
            if df_goal['end_location_z'][i] > 2.4 or df_goal['end_location_y'][i] < 35 or df_goal['end_location_y'][i] > 45:
                df_goal.drop(i)
            else:
                # 
                dataset.loc[line,'x'] = df_goal['end_location_x'][i]
                dataset.loc[line,'y'] = df_goal['end_location_y'][i]
                dataset.loc[line,'z'] = df_goal['end_location_z'][i]
                dataset.loc[line,'outcome'] = df_goal['outcome'][i]
                if df_goal['outcome'][i] == 'Saved':
                    dataset.loc[line,'color'] = 'orange'
                else:
                    dataset.loc[line,'color'] = 'green'
                line = line + 1
        
        
        # Create the net
        v_nets = 10     # vertical lines
        h_nets = 0.25   # horizontal lines
    while v_nets != 0:
        plt.plot([45-v_nets,45-v_nets],[0,2.6], c='grey', linewidth=.15)
        plt.plot([35,45],[h_nets,h_nets], c='grey', linewidth=.15)
        h_nets += 0.25
        v_nets -= 1
    
    plt.style.use('_mpl-gallery-nogrid')
    # plt.figure(figsize=(12,7))
    
    plt.figure(figsize=(12,7))
    # Ground line
    plt.plot([34.5,45.5],[-0.02,-0.02], c='black',linewidth=5)
    # Create the posts
    plt.plot([35,35],[0,2.6], c='black',linewidth=7)
    plt.plot([45,45],[0,2.6], c='black',linewidth=7)
    plt.plot([35,45],[2.6,2.6], c='black',linewidth=7)
    
    # Import the data
    # plt.scatter(dataset.y, dataset.z, marker='o', c=dataset.color)
    x,y = np.meshgrid(dataset.y, dataset.z)
    z = dataset.y
    ax = plt.subplot()
    ax.contourf(x,y)

    plt.axis('off')
    plt.show()
    
Shot_target(pathfile='Lineups_JSON/*', team_name='Barcelona')
