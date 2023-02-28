import locale
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from bs4 import BeautifulSoup
import requests
import string


def WorldCup_competitors():

    def supprime_accent(ligne):
            """ supprime les accents du texte source """
            accents = { 'a': ['à', 'ã', 'á', 'â'],
                        'e': ['é', 'è', 'ê', 'ë'],
                        'i': ['î', 'ï'],
                        'u': ['ù', 'ü', 'û'],
                        'o': ['ô', 'ö'] }
            for (char, accented_chars) in accents.items():
                for accented_char in accented_chars:
                    ligne = ligne.replace(accented_char, char)
            return ligne



    # Phases of the world cup
    cdm = pd.read_excel('CDM/CDM2022.xlsx')

    # URL link 
    url = 'https://www.lequipe.fr/Football/fifa/page-ranking-equipes/general'

    # Requests
    page = requests.get(url)
    data = page.text
    soup = BeautifulSoup(data, 'html.parser')

    # Retrieving the html tag containing the country name
    ahref = soup.find_all('a', class_="Link table__link")

    data=[]
    for e in ahref :
        e=e.text
        data.append(e.strip())

    poule = pd.DataFrame({'rank':[i for i in range(1,len(data)+1)],'country':data})

    group = []
    for i in cdm.Groupe.unique():
        group.extend([i]*4)

    countries = []
    for i in poule.country.unique():
        countries.append(supprime_accent(i))

    # print(cdm.Equipe.unique())
    idx = 0
    for k in cdm.Equipe.unique():
        for i in range(len(poule)):
            if countries[i] == k:
                poule.loc[i,'group'] = group[idx]
                idx = idx + 1

    # Set up the dataframe
    team_competition = pd.DataFrame(poule[(poule.group == 'A')].sort_values(by='rank').reset_index(drop='True'))
    for k in list(string.ascii_uppercase)[1:8]:
        team_competition = team_competition.append(poule[(poule.group == k)].sort_values(by='rank'), ignore_index=True)

    return team_competition 


