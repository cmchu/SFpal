from flask import Flask, request, jsonify,render_template, redirect, url_for
from sklearn.metrics import jaccard_similarity_score

import pandas as pd

app = Flask(__name__)


def predict(input):

    for row in range(gold_standard.shape[0]):
        similarity = jaccard_similarity_score(gold_standard.drop(["similarity", "zip"], axis=1).ix[row,],input)
        gold_standard.ix[row, "similarity"] = similarity

    return gold_standard.sort_values("similarity", ascending=False).reset_index(drop=True).ix[[0, 1, 2], "zip"]


@app.route('/', methods=['GET', 'POST'])
def default():
    #output = dict()
    out = [('Best', 94116), ('Better Than Good', 94112), ('Good', 94127)]
    # this could be a web page of docs instead
    #output['message'] = 'Welcome to the SFpal!'
    if request.method == "POST":
        if request.form['submit'] == 'submit':
            selected_val = ','.join(request.form.getlist('check'))
            return redirect(url_for('.do_result', selected_val=selected_val))
    return render_template('index_3.html')


@app.route('/result')
def do_result():
    selected_val = request.args['selected_val']
    # replace this with a query from whatever database you're using
    val = selected_val.split(",")

    out = get_community(val)

    #return jsonify(out)
    return render_template('result.html', scroll='something', out=out)
    #return redirect(url_for('.default', _anchor="services", out = out))

   
@app.route('/Ready')
def post_history():

    # return a json to see all the variable inputs
    out = request.args.to_dict()

    return jsonify(out)


@app.route('/SFpal')
def get_community(selected):

    keys = ["sanitation", "peace_quiet", "appearance", "children_friendly", "greenery", "walking_cxcondition", "coffee", "nightlife", "dog_friendly", "construction", "parks", "schools", "bart_stations", "safety", "restaurants"]
    vals = [1.0 if i in selected else 0.0 for i in keys]
    prediction = predict(vals)
    out = zip(['Best', 'Better Than Good', 'Good'], prediction)

    return out


if __name__ == "__main__":

    gold_standard = pd.read_csv('gold_standard.csv')
    app.run(host='0.0.0.0')# need this to access from the outside world!
