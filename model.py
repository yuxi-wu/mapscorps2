import pandas as pd
import statsmodels.formula.api as sm
from util import get_area, get_scores
from apikey import *
import math

chicago = pd.read_csv('chicago_training.csv', encoding='utf-8-sig')

result = sm.ols(formula=\
    'workers_weeks ~ area + walkscore + transitscore + bikescore',\
    data=chicago).fit()

model = dict(result.params)

def predictor_chi(neighbourhood, city, state):
    googlequery = neighbourhood + ' ' + city + ' ' + 'state'
    area = get_area(gmclient, googlequery)


    walkscore, transitscore, bikescore = get_scores(neighbourhood, city, state)

    workers_weeks = model['Intercept'] + model['area']*area + \
        model['walkscore']*walkscore + model['transitscore']*transitscore + \
        model['bikescore']*bikescore

    return math.ceil(workers_weeks)
