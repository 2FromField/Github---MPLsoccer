import json
import glob
import pandas as pd
import numpy as np

def GetStats(globPath):
    '''
    Generate 2 dataframes:
        [0] : All stats per season per team
        [1] : Average stats of all seasons per team
        
    Parameters:
        globPath (str) : path to the folder containing all the JSON files of the regular seasons
        
    Returns: 
        2 dataframes: [0],[1]
    '''
    
    # Final dataframe [0]
    df_ALLStats = pd.DataFrame([], columns=['team','average_goal','win [%]','home_win [%]','visitor_win [%]'])

    # Run all the files
    for filename in glob.glob(f'{globPath}*.json'):
        # Open each file
        with open(f'{filename}') as file:
            data = json.load(file)


        ##########################################
        ######### RAW DATA OF THE SEASON #########
        ##########################################
        df_perSEASON = pd.DataFrame([], columns=['week','competition','season','stadium','home_team','home_score','visitor_score','visitor_team'])
        
        line = 0
        # Browse all the matches
        for match in range(len(data)):
            #### COMPETITION INFORMATIONS
            df_perSEASON.loc[line,'competition'] = data[match]['competition']['competition_name']
            df_perSEASON.loc[line, 'season'] = data[match]['season']['season_name']
            df_perSEASON.loc[line,'week'] = data[match]['match_week']
            df_perSEASON.loc[line,'stadium'] = str(data[match]['stadium']['name'])+'('+str(data[match]['stadium']['country']['name'])+')'

            #### HOME INFORMATIONS
            df_perSEASON.loc[line,'home_team'] = str(data[match]['home_team']['home_team_name'])+' ('+str(data[match]['home_team']['country']['name'])+')'
            df_perSEASON.loc[line,'home_score'] = data[match]['home_score']
            
            #### VISITOR INFORMATIONS
            df_perSEASON.loc[line,'visitor_team'] = str(data[match]['away_team']['away_team_name'])+' ('+str(data[match]['away_team']['country']['name'])+')'
            df_perSEASON.loc[line,'visitor_score'] = data[match]['away_score']        
            #
            line += 1

        # Sort the dataframes per week 
        df_perSEASON = df_perSEASON.sort_values(by=['week']).reset_index(drop=True)
        
        #print(df_perSEASON)



        ##################################
        ######### SEASON'S STATS #########
        ##################################
        # List of all regular season team
        teams = df_perSEASON.home_team.unique()

        df_statsPERseason = pd.DataFrame([], columns=['team','season','average_goal','win [%]','home_win [%]','visitor_win [%]'])

        line_stats = 0
        for i in range(len(teams)):
            goals = []
            win = []
            visitor_win = []
            home_win = []
            for k in range(len(df_perSEASON.index)):
                if teams[i] == df_perSEASON.home_team[k]:
                    goals.append(df_perSEASON.home_score[k])
                    #
                    if df_perSEASON.home_team[k] > df_perSEASON.visitor_team[k]:
                        win.append(1)
                        home_win.append(1)
                    else:
                        win.append(0)
                        home_win.append(0)
                elif teams[i] == df_perSEASON.visitor_team[k]:
                    goals.append(df_perSEASON.visitor_score[k])
                    #
                    if df_perSEASON.visitor_team[k] > df_perSEASON.home_team[k]:
                        win.append(1)
                        visitor_win.append(1)
                    else:
                        win.append(0)
                        visitor_win.append(0)
            
            # Calculation of the average stats    
            df_statsPERseason.loc[line_stats,'win [%]'] = round(np.mean(win)*100,1)
            df_statsPERseason.loc[line_stats,'home_win [%]'] = round(np.mean(home_win)*100,1)
            df_statsPERseason.loc[line_stats,'visitor_win [%]'] = round(np.mean(visitor_win)*100,1)
            df_statsPERseason.loc[line_stats,'team'] = teams[i]
            df_statsPERseason.loc[line_stats,'average_goal'] = round(np.mean(goals),1)
            line_stats += 1
        
        df_statsPERseason.season = [df_perSEASON.season[0]]*len(df_statsPERseason)
        
        #print(df_statsPERseason)


        ####################################
        ######### STATS PER SEASON #########
        ####################################
        if len(df_ALLStats) == 0:
            df_ALLStats= df_statsPERseason
        elif len(df_ALLStats) > 1:
            # Adds the new season to the dataframe
            df_ALLStats= pd.concat([df_ALLStats,df_statsPERseason])

    df_ALLStats = df_ALLStats.sort_values(by=['season']).reset_index(drop=True)
    #print(df_ALLStats)


    ########################################
    ######### STATS OF ALL SEASONS #########
    ########################################
    # Final dataframe [1]
    df_StatsAllSeason = pd.DataFrame([], columns=['team','average_goal','win [%]','home_win [%]','visitor_win [%]'])

    all_teams = df_ALLStats.team.unique()
    
    line_season = 0
    for k in range(len(all_teams)):
        df_StatsAllSeason.loc[line_season,'team'] = df_ALLStats[(df_ALLStats.team == all_teams[k])]['team'].tolist()[0]
        df_StatsAllSeason.loc[line_season,'average_goal'] = round(np.mean(df_ALLStats[(df_ALLStats.team == all_teams[k])]['average_goal'].tolist()),1)
        df_StatsAllSeason.loc[line_season,'win [%]'] = round(np.mean(df_ALLStats[(df_ALLStats.team == all_teams[k])]['win [%]'].tolist()),1)
        df_StatsAllSeason.loc[line_season,'home_win [%]'] = round(np.mean(df_ALLStats[(df_ALLStats.team == all_teams[k])]['home_win [%]'].tolist()),1)
        df_StatsAllSeason.loc[line_season,'visitor_win [%]'] = round(np.mean(df_ALLStats[(df_ALLStats.team == all_teams[k])]['visitor_win [%]'].tolist()),1)
        #
        line_season += 1
    
    df_StatsAllSeason = df_StatsAllSeason.sort_values(by=['team']).reset_index(drop=True)
    #print(df_StatsAllSeason)
    return df_ALLStats,df_StatsAllSeason


AllStats = GetStats('Matches_JSON/')[0]
AverageAllStats = GetStats('Matches_JSON/')[1]

print(AllStats)
print(AverageAllStats)
