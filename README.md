### Community Action Bureau / MAPSCorps
### Project 2 - Worker Productivity Model

#### Instructions
1. Type "zip code" or "city" into box 1.  (Sadly no dropdown menu yet...I can fix this later).
2. Type the city name, zip code, or list of zip codes into box 2.  Separate multiple zip codes with commas, e.g. "60637,60615,60602".
3. Type in the two letter abbreviation of the state.
4. Submit!

Currently I have removed support for neighbourhoods, because I haven't found a good data source that captures all the ZIP codes or census tracts within a neighbourhood since they differ so much from city to city.  This made it hard to find the number of places in a neighbourhood, and since that's the most important factor of the regression model I felt it was best to leave it out.  This is probably something that could be built into a database later.

#### Caveats:
* Multiple zip code queries will return a result with the sum of all zip codes.  If you want to look at a breakdown then you have to enter each one individually.
* The area returned might be a bit off (or a lot off for large regions like cities) because I'm going off Google Maps lat-long coordinates which basically consist of drawing a giant rectangle at the most extreme points of a region.  So take this with a grain of salt.  But I took this area calculation out of the regression anyway because it wasn't statistically significant, so the number is really for personal reference more than anything else.
* Similarly, walk/transit/bikescores are a little iffy sometimes due to the layout of their website -- some cities get a specific city score, while others aren't big enough and thus get inaccurate scores for specific addresses.  But again, the most significant predictor is number of places anyway.
* Some cities just won't work and I can't figure out why.  But the majority of top cities in the US that I tested did work.  Two I found that didn't are Indianapolis and Nashville.  My guess is that maybe there wasn't data available for them on the economic census.


#### Currently we have:
* clean neighborhood and productivity data for Chicago
* a regression model trained with the following predictors:
  * number of places
  * walkscore, transitscore, bikescore
  * explained variable = number of workers
* a functioning flask app hosted on heroku

#### Datasets:
* lat-long from Google Maps to calculate area
* number of places per city, per zip code from US Economic Census
* walkscore, transitscore, bikescore from walkscore.com
* past productivity data for Chicago

#### Next steps:
* build database for census data in postgres
* find data source for all zip codes in a neighbourhood
