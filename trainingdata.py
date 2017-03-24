import pandas as pd
import googlemaps as gm
import json
import csv
import math
import dfs
from util import get_area, get_scores
from apikey import *


gmclient = gm.client.Client(key=gmkey)

chicago = pd.DataFrame(columns=('geoarea','workers x weeks','area','num_places',\
    'walkscore','transitscore','bikescore'))

def get_chi_training_data():
    for i in list(dfs.geo_avgs.T):
        if (i == 'Chicago Loop') or (i == 'Loop'):
            pass
        else:
            i_places = dfs.places['GeoArea'] == i

            workers = list(dfs.places[i_places]['MappedUser'].value_counts())
            workers_x_weeks = 1
            if len(workers) > 0:
                workers = sum(workers) / max(workers)
                workers_x_weeks = math.ceil(dfs.geo_avgs['weeks'][i] * workers)

            if i == 'Mckinley Park':
                i = 'McKinley Park'

            n = i + ' Chicago IL'
            area = get_area(gmclient, n)

            num_places = len(dfs.places[i_places])

            geo_url = '/IL/Chicago/{}'.format('_'.join(i.split()))

            walkscore, transitscore, bikescore = get_scores(geo_url)

            chicago.loc[len(chicago)] = \
                (i, workers_x_weeks, area, num_places, \
                walkscore, transitscore, bikescore)

def go():
    get_chi_training_data()
    chicago = chicago.rename(columns={'workers x weeks':'workers_weeks'})
    chicago = chicago.set_index('geoarea')
    chicago.to_csv('chicago_training.csv')

if __name__ == "__main__":
    go()
