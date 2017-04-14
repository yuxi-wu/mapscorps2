from flask import render_template, request
from model_flask import app
from form import UrlForm
from test import tester
from model import predictor_chi

@app.route("/model")
@app.route('/')
def homepage():
    print('routed correctly')
    form = UrlForm()
    return render_template('bias_buster_home.html',
                           title="Worker Predictor",
                           form=form)

@app.route("/results", methods=["post"])
def results():
    #print(request.form["url"])
    try:
        data = predictor_chi(request.form['PType'],\
            request.form['Place'], request.form['State'])
        query = data['query']
        walkscore = data['walkscore']
        transitscore = data['transitscore']
        bikescore = data['bikescore']
        workers = data['workers']
        num_places = data['num_places']
        print(data)
    except AssertionError:
        data = {'none': ['The news source is not in our database; please enter another article from different news source.']}
    #data = {'source name': ['center', 'http://thisisafakelink.com', 'title?']}
    # data = tester(request.form["url"])
    return render_template("bias_buster_results.html", data=data)
