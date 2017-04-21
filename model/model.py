import pandas as pd
import statsmodels.formula.api as sm
from .util import calculate_area, get_scores, get_zip_places, get_city_places
from .apikey import *
import math

chicago = pd.read_csv('./model/chicago_training.csv', encoding='utf-8-sig')

result = sm.ols(formula=\
    'workers_weeks ~ num_places + walkscore + transitscore + bikescore',\
    data=chicago).fit()

model = dict(result.params)

def predictor_chi(place_type, places, state):
    place_type = place_type.upper()
    places = places.title().split(',')
    walkscore, transitscore, bikescore = 0,0,0

    if (place_type == 'NEIGHBOURHOOD') or (place_type == 'ZIP Code'):
        googlequery = [p + ' ' + state for p in places]
        areas = [calculate_area(gmclient, gq) for gq in googlequery]
        area = sum(areas)
        scores = [get_scores(p, place_type) for p in places]
        walkscore = sum([s[0] for s in scores]) / len(places)
        transitscore = sum([s[1] for s in scores]) / len(places)
        bikescore = sum([s[2] for s in scores]) / len(places)

        if place_type == 'ZIP CODE':
            n_p_list = [get_zip_places(p) for p in places]
            num_p = sum(n_p_list)

    elif place_type == 'CITY':
        googlequery = places[0] + ' ' + state
        area = calculate_area(gmclient, googlequery)
        walkscore, transitscore, bikescore = get_scores(places[0],place_type,state)
        num_p = get_city_places(places[0], state)

    workers_weeks = model['Intercept'] \
        + model['num_places']*num_p \
        + model['walkscore']*walkscore \
        + model['transitscore']*transitscore \
        + model['bikescore']*bikescore

    results = {'query': '{}, {}'.format(','.join(places),state), \
        'num_places':num_p,\
        'walkscore':'%.2f' % walkscore, \
        'transitscore':'%.2f' % transitscore, \
        'bikescore':'%.2f' % bikescore,
        'area':'{} sq miles'.format('%.2f' % area), \
        'workers':math.ceil(workers_weeks)}

    return results

'''def go(place_type, place, city=None, state):
    if place_type == 'City':'''
