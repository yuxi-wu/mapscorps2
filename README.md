### Community Action Bureau / MAPSCorps
### Project 2 - Worker Productivity Model

#### Instructions
1. navigate to 'mapscorps2' directory via cd / command line
2. type into command line 'python3 model_flask.py'
3. visit 'localhost:5001' in browser

#### Currently we have:
* clean neighborhood data for Chicago
* a regression model trained with:
  * number of places
  * area of a given region
  * walkscore, transitscore, bikescore
* a functioning flask app

#### Next steps:
* build database for census data in postgres
* write function to call economic census data on the fly
* think about granularity - how small do we want to get? ZIP code? block?
  * smallest scale for num_places is ZIP
  * we can get neighborhood characteristics down to the block though
* get all ZIP codes of one city to avoid API blocks on census
* include option for multiple regions
