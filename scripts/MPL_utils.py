import pandas as pd
import re
import numpy as np

def get_nationalities():
    """ 
    Returns a python dictionary with the full country name as key and its abbreviation as value
    """
    fichier = open("Scripts_Tools/Nationalities.txt", "r").read()

    nationalities = {}
    split_fichier = fichier.split('\n')

    for i in split_fichier:
        stringer = ''
        for k in range(len(i)):
            if i[k] != ':':
                stringer = stringer + i[k]
            else:
                nationalities[stringer] = i[k+1:]
                continue
    
    return nationalities


def get_placements():
    """ 
    Returns a python dictionary with the full country name as key and its abbreviation as value
    """
    fichier = open("Scripts_Tools/Placements_on_field.txt", "r").read()

    placements = {}
    split_fichier = fichier.split('\n')

    for i in split_fichier:
        stringer = ''
        for k in range(len(i)):
            if i[k] != ':':
                stringer = stringer + i[k]
            else:
                placements[stringer] = tuple(list(np.float_(i[k+2:-1].split(','))))
                continue
    
    return placements
