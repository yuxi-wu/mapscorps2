from bs4 import BeautifulSoup, SoupStrainer
import certifi
import urllib3
import ast
import pandas as pd
import string
from googlemaps import geocoding as gc
from math import radians, cos, sin, asin, sqrt
from .apikey import *

def get_soup(url):
    '''
    Returns BeautifulSoup object of a given url.
    Input: url (str).
    Output: BeautifulSoup object.
    '''
    pm = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    html = pm.urlopen(url=url, method="GET").data
    return BeautifulSoup(html, "lxml")

def get_strained_soup(url, tag, attr=None):
    '''
    Returns a filtered BeautifulSoup object with SoupStrainer.
    Inputs:
        - url (str).
		- tag (str) = HTML tag that user wishes to retrieve.
		- attr (dict) = attributes of above HTML tag.
    Output: strained BeautifulSoup object.
    '''
    pm = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    html = pm.urlopen(url=url, method="GET").data
    if attr:
        strained = SoupStrainer(tag, attrs=attr)
    else:
        strained = SoupStrainer(tag)
    return BeautifulSoup(html, "lxml", parse_only=strained)

def get_scores(place, place_type, state=None):
    if (place_type == 'Neighbourhood') or (place_type == 'ZIP Code'):
        fullurl = 'https://www.walkscore.com/score/' + '_'.join(place.split())
        ws = get_strained_soup(fullurl, 'img').find(alt='Walk Score of this location')
        ts = get_strained_soup(fullurl, 'img').find(alt='Transit Score of this location')
        bs = get_strained_soup(fullurl, 'img').find(alt='Bike Score of this location')
        if (not ws) and (not ts) and (not bs):
            address = get_soup(fullurl).find(class_='badges-link-upper-right float-right-noncleared badges-link medsmallfont small-pad-top').\
                findNext('a')['href'].strip('/professional/badges.php?address=')
            address = "".join(l for l in address if l not in string.punctuation)
            print(address)
            ws = get_strained_soup(fullurl, 'img').find(alt='Walk Score of {}'.format(address))
            ts = get_strained_soup(fullurl, 'img').find(alt='Transit Score of  {}'.format(address))
            bs = get_strained_soup(fullurl, 'img').find(alt='Bike Score of  {}'.format(address))
    elif place_type == 'City':
        fullurl = 'https://www.walkscore.com/{}/{}'.format(state, place)
        ws = get_strained_soup(fullurl, 'img').find(alt='Walk Score of {}, {}'.format(place,state))
        ts = get_strained_soup(fullurl, 'img').find(alt='Transit Score of {}, {}'.format(place,state))
        bs = get_strained_soup(fullurl, 'img').find(alt='Bike Score of {}, {}'.format(place,state))

    wscore = 0
    tscore = 0
    bscore = 0

    if ws:
        wscore = int(ws['src'].strip('//pp.walk.sc/badge/walk/score/').strip('.svg'))
    if ts:
        tscore = int(ts['src'].strip('//pp.walk.sc/badge/transit/score/').strip('.svg'))
    if bs:
        bscore = int(bs['src'].strip('//pp.walk.sc/badge/bike/score/').strip('.svg'))
    return wscore, tscore, bscore

def get_centre_coordinates(gm, geoarea):
    coords = gc.geocode(gm, address=geoarea)[0]['geometry']['location']
    lat = location['lat']
    lng = location['lng']
    return lat, lng

def get_area_coordinates(gm, geoarea):
    nesw = gc.geocode(gm, address=geoarea)[0]['geometry']['viewport']
    nelat = nesw['northeast']['lat']
    nelng = nesw['northeast']['lng']
    swlat = nesw['southwest']['lat']
    swlng = nesw['southwest']['lng']
    return nelng, nelat, swlng, swlat

def haversine(lng1, lat1, lng2, lat2):
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
    diff_lng = lng2 - lng1
    diff_lat = lat2 - lat1
    a = sin(diff_lat/2)**2 + (cos(lat1) * cos(lat2) * sin(diff_lng/2)**2)
    c = 2 * asin(sqrt(a))
    r = 3963.1676 #radius of earth in miles
    return c * r

def calculate_area(gm, geoarea):
    lng1, lat1, lng2, lat2 = get_area_coordinates(gm, geoarea)
    length = haversine(lng1, lat1, lng1, lat2)
    width = haversine(lng1, lat1, lng2, lat1)
    return length * width

def get_num_places(api_url):
    pm = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    r = pm.urlopen(url=api_url, method="GET").data
    l = ast.literal_eval(r.decode('utf8'))
    if 'zbp' in api_url:
        n = l[1][0]
    elif 'ewks' in api_url:
        n = 0
        a = [i for i in l if len(i[2])==2 if i[1]=='A']
        for i in a:
            n += int(i[0])
    return int(n)

def get_zip_places(zipcode):
    url = 'http://api.census.gov/data/2014/zbp?get=ESTAB&for=zipcode:{}&NAICS2012=00'\
        .format(zipcode)
    return get_num_places(url)

def get_city_fips(city, state):
    fips = pd.read_csv('./model/fips_codes_places.csv')
    fips.columns = [i.strip('\ufeff') for i in fips.columns]
    df = (fips['GU Name'] == city) & (fips['Entity Description'] == 'city') \
        & (fips['State Abbreviation'] == state)
    cityfips = fips[df].iloc[0]['FIPS Entity Code']
    statefips = fips[df].iloc[0]['State FIPS Code']
    return cityfips,statefips

def get_city_places(city,state):
    c,s = get_city_fips(city,state)
    url = 'http://api.census.gov/data/2012/ewks?get=ESTAB,OPTAX&NAICS2012=*&key={}&in=state:{}&for=place:{}'.format(censuskey,s,c)
    return get_num_places(url)

def get_city_zips(city, state):
    url = 'http://www.getzips.com/cgi-bin/ziplook.exe?What=2&City={}&State={}&Submit=Look+It+Up'.format(city,state)
    soup = get_strained_soup(url,'td')
    zips = [z.text for z in soup.find_all('td', width="15%") if z.text!='ZIP']
    return zips
