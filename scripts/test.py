import json
import pandas as pd

with open('Lineups_JSON/lineups_15946.json') as file:
    data = json.load(file)

lineup_away_team = data[1]['lineup']

df_lineups_away = pd.DataFrame([], columns=[])
time_laps = ['00:00', '45:00', '67:42', '68:14', '70:22', '76:14', '76:18', '84:07', '84:22', '90:00']

line_away = 0
for away_players in range(len(lineup_away_team)):
    for p in range(len(lineup_away_team[away_players]['positions'])):
        df_lineups_away.loc[line_away,'player'] = lineup_away_team[away_players]['player_name']
        df_lineups_away.loc[line_away,'nickname'] = lineup_away_team[away_players]['player_nickname']
        df_lineups_away.loc[line_away,'position'] = lineup_away_team[away_players]['positions'][p]['position']
        df_lineups_away.loc[line_away,'from'] = lineup_away_team[away_players]['positions'][p]['from']
        df_lineups_away.loc[line_away,'to'] = lineup_away_team[away_players]['positions'][p]['to']
        df_lineups_away.loc[line_away,'nationality'] = lineup_away_team[away_players]['country']['name']
        df_lineups_away.loc[line_away,'number'] = lineup_away_team[away_players]['jersey_number']
        df_lineups_away.loc[line_away,'player_id'] = lineup_away_team[away_players]['player_id']
        line_away += 1

df_lineups_away.to = df_lineups_away.to.replace({None:'90:00'})

print(df_lineups_away)

for j in time_laps[1:]:
    print(j)
    print(df_lineups_away[(df_lineups_away['to'] >= j) & (df_lineups_away['from'] < j)].reset_index(drop=True))

            