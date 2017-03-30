import pandas as pd
import statsmodels.formula.api as sm
from .util import get_area, get_scores
from .apikey import *
import math

chicago = pd.read_csv('./model/chicago_training.csv', encoding='utf-8-sig')

result = sm.ols(formula=\
    'workers_weeks ~ area + num_places + walkscore + transitscore + bikescore',\
    data=chicago).fit()

model = dict(result.params)

def predictor_chi(neighbourhood, city, state):
    neighbourhood = neighbourhood.title()
    city = city.title()
    state = state.upper()

    googlequery = neighbourhood + ' ' + city + ' ' + state
    area = get_area(gmclient, googlequery)
    print(neighbourhood, city, state)
    walkscore, transitscore, bikescore = get_scores(neighbourhood, city, state)

    workers_weeks = model['Intercept'] + model['area']*area + \
        model['walkscore']*walkscore + model['transitscore']*transitscore + \
        model['bikescore']*bikescore

    results = {'query': '{}, {}, {}'.format(neighbourhood,city,state),\
        'walkscore':walkscore, 'transitscore':transitscore, 'bikescore':bikescore,
        'area':area, 'workers':math.ceil(workers_weeks)}

    return results
