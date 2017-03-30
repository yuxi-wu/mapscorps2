import pandas as pd

targs = pd.read_csv('../chi_csv/targs.csv',encoding='utf-8-sig')
targs = targs.set_index('Team Name')
geos = pd.read_csv('../chi_csv/geo_percent.csv',encoding='utf-8-sig')
ind = pd.read_csv('../chi_csv/individuals.csv',encoding='utf-8-sig')
ind = ind.set_index('Username')

#INDIVIDUAL AVERAGES - MAPPING
ind_map = pd.DataFrame()
ind_map['wk_avg'] = ind.T[2:7].T.mean(axis=1)
ind_map['day_avg'] = ind_map['wk_avg'] / 5
#INDIVIDUAL AVERAGES - FC
ind_fc = pd.DataFrame()
ind_fc['wk_avg'] = ind.T[7:12].T.mean(axis=1)
ind_fc['day_avg'] = ind_fc['wk_avg'] / 5
#INDIVIDUAL AVERAGES - CHECKING
ind_check = pd.DataFrame()
ind_check['wk_avg'] = ind.T[12:17].T.mean(axis=1)
ind_check['day_avg'] = ind_check['wk_avg'] / 5
#GEOAREA AVERAGES
geo_avgs = pd.read_csv('../chi_csv/dayweekgeo.csv',encoding='utf-8-sig')
geo_avgs = geo_avgs.set_index('geoarea').fillna(0)

places = pd.read_csv('../chi_csv/actualplaces.csv',encoding='utf-8-sig')

'''
need to figure out what geoprod was...
placecounts = geoprod['GeoAreaName'].value_counts() #places per geoareaprod
mapped = geoprod['Description'] == 'Mapped'
allmapped = geoprod[mapped]
'''
