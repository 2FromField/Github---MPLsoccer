import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def EventStats_XLSX(filename):
    """ Return a list of 2 dictionnaires, 1 for each team, with the statistics of each event

    Args:
        filename (str): path to the Excel file

    Returns:
        Stats for each event in the match in the form of a pizza chart
    """
    # Database
    data = pd.read_excel(filename,sheet_name='data')
    lst = []
    
    # Match teams
    home_team = data.team_name.unique()[0]
    away_team = data.team_name.unique()[1]   
    teams = [home_team,away_team]
    
    # List of events
    events = ['Carry','Miscontrol','Foul Committed','Substitution','Clearance',
              'Duel','Interception','Dribble','Pass','Shot']
    
    for team in teams:
        dict_team = {'team':team}
        #
        for event in events:
            #
            if event == 'Carry':
                df_team = data[(data.team_name == team) & (data.type_name == event)].reset_index(drop=True)
                df_event = data[(data.type_name == event)].reset_index(drop=True)
                #

                dict_team[event] = round((len(df_team)*100)/(len(df_event)),1)
            
            #
            df = data[(data.team_name == team) & (data.type_name == event)].reset_index(drop=True)

            ## Miscontrol or Foul Committed or Substitution or Clearance ##
            liste1 = ['Miscontrol','Foul Committed','Substitution','Clearance','Tactical Shift']
            for k in liste1 :
                if event == k:
                    dict_team[event] = len(df)

            ## DUEL ##
            liste2 = ['Duel','Interception']
            for j in liste2:
                if event == j:
                    incompleted = 0
                    completed = 0
                    for h in range(len(df.index)):
                        if isinstance(df.outcome_name[h], float):
                            continue
                        else:
                            if df.outcome_name[h].startswith('Lost'):
                                incompleted += 1
                            else:
                                completed += 1
                                
                    dict_team[f'{event}_incompleted'] = incompleted
                    dict_team[f'{event}_completed'] = completed
                
            ## DRIBBLE ##
            if event == 'Dribble':
                dict_team[f'{event}_completed'] = len(df[(df.outcome_name == 'Complete')].reset_index(drop=True))
                dict_team[f'{event}_incompleted'] = len(df[(df.outcome_name == 'Incomplete')].reset_index(drop=True))
            
            ## PASS ##
            if event == 'Pass':
                completed = 0
                for i in range(len(df)):
                    if isinstance(df.outcome_name[i], float):
                        completed += 1
                dict_team[f'{event}_completed'] = completed
                dict_team[f'{event}_incompleted'] = len(df[(df.outcome_name == 'Incomplete')])
            
            ## SHOT ##
            if event == 'Shot':
                dict_team[f'{event}_completed'] = len(df[(df.outcome_name == 'Goal')].reset_index(drop=True))
                dict_team[f'{event}_incompleted'] = len(df[(df.outcome_name != 'Goal')])

        # Append
        lst.append(dict_team)
    
    # Return
    return lst
def percentage(value,max_value):
    try:
        result = (value*100)/(max_value)
    except ZeroDivisionError:
        result = 0
    else:
        result = (value*100)/(max_value)
    return result

# data
stats = EventStats_XLSX('MatchEvents_XLSX/MatchID_9636.xlsx')


# Teams
home = stats[0]['team']
away = stats[1]['team']
lw_axv = 40


## PYRAMID CHART ##
df = pd.DataFrame({'Stats': ['Shot','Pass [%]','Interception [%]','Dribble [%]','Duel [%]',
                           'Possession [%]','Substitution','Foul Committed','Clearance'], 
                    home: [-(stats[0]['Shot_completed']+stats[0]['Shot_incompleted'])-lw_axv,
                           -int(percentage(stats[0]['Pass_completed'],(stats[0]['Pass_completed']+stats[0]['Pass_incompleted'])))-lw_axv,
                            -int(percentage(stats[0]['Interception_completed'],(stats[0]['Interception_completed']+stats[0]['Interception_incompleted'])))-lw_axv,
                            -int(percentage(stats[0]['Dribble_completed'],(stats[0]['Dribble_completed']+stats[0]['Dribble_incompleted'])))-lw_axv,
                            -int(percentage(stats[0]['Duel_completed'],(stats[0]['Duel_completed']+stats[0]['Duel_incompleted'])))-lw_axv,
                            #
                            -stats[0]['Carry']-lw_axv,      -stats[0]['Substitution']-lw_axv,   -stats[0]['Foul Committed']-lw_axv,     -stats[0]['Clearance']-lw_axv], 
                    away: [(stats[1]['Shot_completed']+stats[1]['Shot_incompleted'])+lw_axv,
                            int(percentage(stats[1]['Pass_completed'],(stats[1]['Pass_completed']+stats[1]['Pass_incompleted'])))+lw_axv,
                            int(percentage(stats[1]['Interception_completed'],(stats[1]['Interception_completed']+stats[1]['Interception_incompleted'])))+lw_axv,
                            int(percentage(stats[1]['Dribble_completed'],(stats[1]['Dribble_completed']+stats[1]['Dribble_incompleted'])))+lw_axv,
                            int(percentage(stats[1]['Duel_completed'],(stats[1]['Duel_completed']+stats[1]['Duel_incompleted'])))+lw_axv,
                            #
                            stats[1]['Carry']+lw_axv,      stats[1]['Substitution']+lw_axv,   stats[1]['Foul Committed']+lw_axv,     stats[1]['Clearance']+lw_axv]})

print(df)


Stats = ['Shot','Pass [%]','Interception [%]','Dribble [%]','Duel [%]','Possession [%]','Substitution','Foul Committed','Clearance']
sns.set(rc={'figure.facecolor':'#23272d'})


bar_plot = sns.barplot(x=home, y='Stats', data=df, order=Stats, color='#4469b1')
bar_plot = sns.barplot(x=away, y='Stats', data=df, order=Stats, color='#9b3838')


# stats name
line_stats = 0.1
for i in df.Stats:
    plt.text(0, line_stats, i, size=10, color="whitesmoke", ha='center')
    line_stats += 1


# stats values
line_score = 0.1
for k in range(len(Stats)):
    plt.text(df[f'{home}'][k]-15, line_score, round(abs(df[f'{home}'][k]+lw_axv)), size=12, color="whitesmoke")
    plt.text(df[f'{away}'][k]+5, line_score, round(df[f'{away}'][k]-lw_axv), size=12, color="whitesmoke")
    line_score += 1

# teams
plt.text(70, -1.1, f" {away}", size=15, color="whitesmoke", ha='center', fontweight='bold')
plt.text(-70, -1.1, f"{home}", size=15, color="whitesmoke", ha='center', fontweight='bold')
# score
plt.text(10, -1.1, f"{stats[1]['Shot_completed']}", size=15, color="whitesmoke", ha='center', fontweight='bold')
plt.text(0, -1.1, f":", size=15, color="whitesmoke", ha='center', fontweight='bold')
plt.text(-10, -1.1, f"{stats[0]['Shot_completed']}", size=15, color="whitesmoke", ha='center', fontweight='bold')

# Copyright
plt.text(130, 9.5, f"Copyright: 2FromField", size=10, color="whitesmoke", ha='center', fontstyle='italic')

plt.axvline(0, c='#23272d', lw=80)
plt.axis('off')

plt.show()






