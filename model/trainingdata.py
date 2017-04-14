import pandas as pd
import json
import csv
import math
import dfs
from util import calculate_area, get_scores
from apikey import *

def get_chi_training_data(chi_df):
    for i in list(dfs.geo_avgs.T):
        if (i == 'Chicago Loop') or (i == 'Loop'):
            pass
        else:
            i_places = dfs.places['GeoArea'] == i

            workers = list(dfs.places[i_places]['MappedUser'].value_counts())*4
            if len(workers) > 0:
                workers = math.ceil(sum(workers) / max(workers))
            else:
                workers = 0

            if i == 'Mckinley Park':
                i = 'McKinley Park'

            n = i + ' Chicago'
            area = calculate_area(gmclient, n)
            num_places = len(dfs.places[i_places])
            walkscore, transitscore, bikescore = get_scores(n, 'Neighbourhood', 'IL')

            chi_df.loc[len(chi_df)] = \
                (i, workers, area, num_places, \
                walkscore, transitscore, bikescore)

def go():
    chicago = pd.DataFrame(columns=('geoarea','workers_weeks','area','num_places',\
        'walkscore','transitscore','bikescore'))
    get_chi_training_data(chicago)
    chicago = chicago.set_index('geoarea')
    chicago.to_csv('chicago_training.csv')

if __name__ == "__main__":
    go()
