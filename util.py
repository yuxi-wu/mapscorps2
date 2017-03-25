from bs4 import BeautifulSoup, SoupStrainer
import certifi
import urllib3
import re
from googlemaps import geocoding as gc
from math import radians, cos, sin, asin, sqrt

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

def get_scores(neighbourhood, city, state):
    ws_url = '/{}/{}/{}'.format(state, '_'.join(city.split()), \
        '_'.join(neighbourhood.split()))
    fullurl = 'https://www.walkscore.com' + ws_url
    soup = get_strained_soup(fullurl,'td')
    scores = soup.find('a',href=ws_url)
    if scores:
        walkscore = scores.find_next('td')
        transitscore = walkscore.find_next('td')
        bikescore = transitscore.find_next('td')
        return int(walkscore.text.strip()), int(transitscore.text.strip()), int(bikescore.text.strip())
    else:
        fullurl = 'https://www.walkscore.com/score/' + \
            '-'.join(neighbourhood.split() + city.split())

        ws = get_strained_soup(fullurl, 'img').find(alt='Walk Score of this location')
        walkscore = 0
        if ws:
            walkscore = int(ws['src'].strip('//pp.walk.sc/badge/walk/score/').strip('.svg'))

        ts = get_strained_soup(fullurl, 'img').find(alt='Transit Score of this location')
        transitscore = 0
        if ts:
            transitscore = int(ts['src'].strip('//pp.walk.sc/badge/transit/score/').strip('.svg'))

        bs = get_strained_soup(fullurl, 'img').find(alt='Bike Score of this location')
        bikescore = 0
        if bs:
            bikescore = int(bs['src'].strip('//pp.walk.sc/badge/bike/score/').strip('.svg'))

        return walkscore, bikescore, transitscore

def get_coordinates(gm, geoarea):
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
    r = 6371 #radius of earth in km
    return c * r

def get_area(gm, geoarea):
    lng1, lat1, lng2, lat2 = get_coordinates(gm, geoarea)
    length = haversine(lng1, lat1, lng1, lat2)
    width = haversine(lng1, lat1, lng2, lat1)
    return length * width
