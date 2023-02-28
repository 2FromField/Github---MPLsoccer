import pandas as pd
import glob
import statsbomb as sb
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn import metrics
import matplotlib.pyplot as plt
from mplsoccer import VerticalPitch

def Predict_Goal(team_name):
    """ Returns the set of shooting positions of the selected team as well as the goal
    prediction percentage according to the shot position on the field

    Args:
        team_name (_str_): Name of the team to be analyzed
    """
    
    
    line = 0
    dataset = pd.DataFrame([], columns=['x','y','target'])

    for filename in glob.glob('Lineups_JSON/*'):
        event_id = filename[21:26]
        events = sb.Events(event_id = f'{event_id}')
        df = events.get_dataframe(event_type = 'shot')
        
        df_goal = df[(df.team == team_name)].reset_index(drop=True)

        for i in range(len(df_goal.index)):
            dataset.loc[line,'x'] = df_goal['start_location_x'][i]
            dataset.loc[line,'y'] = df_goal['start_location_y'][i]
            dataset.loc[line,'target'] = 1 if df_goal.outcome[i] == 'Goal' else 0
            line = line + 1



    pitch= VerticalPitch(pitch_color='grass', line_color='white', half=True)
    fig, ax = pitch.draw(figsize=(10,7))
    # fig.set_size_inches(10,7)
    for i in range(len(dataset.index)):
        if dataset.target[i] == 1:
            goaled = pitch.scatter(dataset.x[i],dataset.y[i], c='blue', marker='o', s=100, ax=ax)
        else:
            ungoaled = pitch.scatter(dataset.x[i],dataset.y[i], c='red', marker='x', s=100, ax=ax)
    plt.legend([goaled, ungoaled], ["Goal","Ungoal"])
    fig.text(0.8,0.935, f'{team_name}', size=20, ha='center', color='white', fontweight='bold')
    fig.text(0.2,0.935, f'Season 2018-19', size=20, ha='center', color='white', fontweight='bold')
    plt.show()


    x = dataset.drop(['target'],axis='columns').to_numpy()
    y = dataset.target.to_numpy().astype('int')

    x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.4, random_state=209)

    cls = svm.SVC(kernel='linear')

    cls.fit(x_train,y_train)

    # Predict the response
    pred = cls.predict(x_test)
    print('Accuracy:', metrics.accuracy_score(y_test,y_pred=pred))

    # Precision score
    print('Precision:', metrics.recall_score(y_test, y_pred=pred))
    print('Score', cls.score(x_test,y_test))

    # Recall score
    print('Recall', metrics.recall_score(y_test,y_pred=pred))
    print(metrics.classification_report(y_test,y_pred=pred))
    
    
    
Predict_Goal(team_name='Barcelona')