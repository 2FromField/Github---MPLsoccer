import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as img
from mplsoccer import PyPizza, add_image


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




###### VISUALISATION #####
stats = EventStats_XLSX('MatchEvents_XLSX/MatchID_9636.xlsx')

def percentage(value,max_value):
    try:
        result = (value*100)/(max_value)
    except ZeroDivisionError:
        result = 0
    else:
        result = (value*100)/(max_value)
    return result


## PIZZA CHART
# Add image 
home_team = stats[0]['team']
photo = img.imread(f'pictures/{home_team.lower()}.png')
logo = img.imread('pictures/Logo_FF.png')

# Titles of each parts
params = [
    "Shot",         "Pass [%]",         "Interception [%]",     "Dribble [%]",      "Duel [%]",
    #
    "Possession [%]",   "Substitution", "Foul Committed",   "Clearance",
    #
    "Shot",         "Pass [%]",         "Interception [%]",     "Dribble [%]",      "Duel [%]"
]

# Values
values = [
    stats[0]['Shot_completed']+stats[0]['Shot_incompleted'],
    int(percentage(stats[0]['Pass_completed'],(stats[0]['Pass_completed']+stats[0]['Pass_incompleted']))),
    int(percentage(stats[0]['Interception_completed'],(stats[0]['Interception_completed']+stats[0]['Interception_incompleted']))),
    int(percentage(stats[0]['Dribble_completed'],(stats[0]['Dribble_completed']+stats[0]['Dribble_incompleted']))),
    int(percentage(stats[0]['Duel_completed'],(stats[0]['Duel_completed']+stats[0]['Duel_incompleted']))),
    #
    stats[0]['Carry'],      stats[0]['Substitution'],   stats[0]['Foul Committed'],     stats[0]['Clearance'],
    #
    stats[1]['Shot_completed']+stats[1]['Shot_incompleted'],
    int(percentage(stats[1]['Pass_completed'],(stats[1]['Pass_completed']+stats[1]['Pass_incompleted']))),
    int(percentage(stats[1]['Interception_completed'],(stats[1]['Interception_completed']+stats[1]['Interception_incompleted']))),
    int(percentage(stats[1]['Dribble_completed'],(stats[1]['Dribble_completed']+stats[1]['Dribble_incompleted']))),
    int(percentage(stats[1]['Duel_completed'],(stats[1]['Duel_completed']+stats[1]['Duel_incompleted'])))
]

compare_values = [
    0,0,0,0,0,
    #
    stats[1]['Carry'],      stats[1]['Substitution'],   stats[1]['Foul Committed'],     stats[1]['Clearance'],
    #
    0,0,0,0,0
]


max_values = [stats[0]['Shot_incompleted']+stats[0]['Shot_incompleted'],
              100,     100,   100,  100,     
              100,   10,    20,     50,
              stats[1]['Shot_incompleted']+stats[1]['Shot_incompleted'],
              100,     100,   100,  100]
min_values = [0]*14


# Color for the slices and text
slice_colors = ["#1A78CF"] * 5 + ['#1A78CF'] * 4 + ["#D70232"] * 5
compare_slice_colors = ["#635f5f"] * 5 + ['#D70232'] * 4 + ["#635f5f"] * 5
text_colors = ["#F2F2F2"] * 10 + ["#F2F2F2"] * 4

# instantiate PyPizza class
baker = PyPizza(
    max_range=max_values,
    min_range=min_values,
    background_color="#222222",
    params=params,                  # list of parameters
    straight_line_color="#222222",  # color for straight lines
    straight_line_lw=2,             # linewidth for straight lines
    last_circle_lw=1,               # linewidth of last circle
    other_circle_lw=1,              # linewidth for other circles
    other_circle_ls="-."            # linestyle for other circles
)

# Plot pizza
fig, ax = baker.make_pizza(
    figsize=(8, 7.5),      
    color_blank_space=["#1b78cf"] * 5 + ['#ffa500'] * 4 + ["#d70132"] * 5,  # background color of the slices
    slice_colors=slice_colors,                                              
    
    #
    values= values,
    value_bck_colors=slice_colors,          
    value_colors=text_colors,
    #
    compare_values= compare_values,
    compare_value_bck_colors=compare_slice_colors,
    compare_colors=compare_slice_colors,
    #
    blank_alpha=0.4,
    kwargs_slices=dict(edgecolor="#000000",
        zorder=2, linewidth=1
    ),         
    kwargs_compare=dict(edgecolor="#000000",
        zorder=2, linewidth=1
    ),                  
    kwargs_params=dict(
        color="#F2F2F2", fontsize=10, va="center"
    ),                
    kwargs_values=dict(
        color="#F2F2F2", fontsize=12, zorder=3,
        bbox=dict(
            edgecolor="#F2F2F2", facecolor="cornflowerblue",
            boxstyle="round,pad=0.2", lw=1
        )
    ),
    kwargs_compare_values=dict(
        color="#F2F2F2", fontsize=12, zorder=3,
        bbox=dict(
            edgecolor="#F2F2F2", facecolor="cornflowerblue",
            boxstyle="round,pad=0.2", lw=1
        )
    )                  
)

# Matplotlib background color
ax.set_facecolor('black')

# Add title
fig.text(
    0.515, 0.97, f"{stats[1]['team']}   {stats[1]['Shot_completed']} - {stats[0]['Shot_completed']}   {stats[0]['team']}", size=20,
    ha="center", color="whitesmoke"
)

# Add subtitle
fig.text(
    0.515, 0.942,
    f"MatchEvents Stats - Copyright: 2FromField",
    size=13,
    ha="center", color="whitesmoke"
)

## LEGENDS ##
fig.patches.extend([
    # Add rectangles
    plt.Rectangle(
        (0, 0.01), 0.5, 0.025, fill=True, color="#d70132",
        transform=fig.transFigure, figure=fig
    ),
    plt.Rectangle(
        (0.5, 0.01), 0.5, 0.025, fill=True, color="#1978cf",
        transform=fig.transFigure, figure=fig
    ),
])

# Add text
fig.text(0.15, 0.015, f" {stats[1]['team']}", size=12, color="whitesmoke")
fig.text(0.7, 0.015, f"{stats[0]['team']}", size=12, color="whitesmoke")


## FromField Image ##
ax_image = add_image(
    photo, fig, left=0.435, bottom=0.425, width=0.15, height=0.135
)

## Team Logo ##
ax_image = add_image(
    logo, fig, left=0.01, bottom=0.88, width=0.13, height=0.127
)

plt.show()
