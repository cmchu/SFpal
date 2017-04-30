from flask import Flask, request, jsonify,render_template, redirect, url_for

app = Flask(__name__)


def predict(input, gold_standard):
    from sklearn.metrics import jaccard_similarity_score

    for row in range(gold_standard.shape[0]):
        similarity = jaccard_similarity_score(gold_standard.drop(["similarity", "zip"], axis=1).ix[row,],input)
        gold_standard.ix[row, "similarity"] = similarity

    return gold_standard.sort_values("similarity", ascending=False).reset_index(drop=True).ix[[0, 1, 2], "zip"]


def get_community(selected, min, max):
    import pandas as pd
    import numpy as np
    import config_appdev
    import get_eta

    keys = ["sanitation", "peace_quiet", "appearance", "children_friendly", "walking_condition", "coffee", "nightlife", "dog_friendly", "construction", "parks", "schools", "bart_stations", "safety", "restaurants"]
    vals = [1.0 if i in selected else 0.0 for i in keys]
    vals.append([int(min), int(max)])
    #===================ADD IN [LAT,LON,driving_boolean] HERE - APPEND TO VALS===========================
    print vals

    gold_standard = pd.read_csv('gold_standard.csv')

    # binarize avg_rent column
    rent_range = vals[-2]
    gold_standard["rent"][(gold_standard["rent"] < rent_range[0]) | (gold_standard["rent"] > rent_range[1])] = 0
    gold_standard["rent"][(gold_standard["rent"] >= rent_range[0]) & (gold_standard["rent"] <= rent_range[1])] = 1
    vals[-2] = 1

    # binarize most frequent destination input/column
    lat_lon = vals[-1]
    if lat_lon[:2] == [0, 0]:
        gold_standard["mindist"] = 0
        vals[-1] = 0
    else:
        API_KEY = config_appdev.API_KEY
        orig_coord = ','.join([str(lat_lon[0]), str(lat_lon[1])])
        eta = get_eta.batch_time(orig_coord, API_KEY, is_driving=lat_lon[2])
        eta["zip"] = eta["zip"].astype(np.int64)
        gold_standard = gold_standard.merge(eta, on="zip", how="left")

        eta_25p = np.nanpercentile(gold_standard["mindist"], q=25)
        gold_standard["mindist"][(gold_standard["mindist"] <= eta_25p)] = 0
        gold_standard["mindist"][(gold_standard["mindist"] > eta_25p)] = 1
        vals[-1] = 1

    # set all NaN values to 0
    gold_standard = gold_standard.fillna(0)

    prediction = predict(vals, gold_standard)
    out = zip(['Best zipcode to live in', 'Second best zipcode to live in', 'Third best zipcode to live in'], prediction)

    return out


@app.route('/', methods=['GET', 'POST'])
def default():

    if request.method == "POST":
        if request.form['submit'] == 'submit':
            min = request.form["min"]
            max = request.form["max"]
            selected_val = ','.join(request.form.getlist('check'))
            return redirect(url_for('.do_result', selected_val=selected_val, min = min, max = max))
    return render_template('index_3.html')


@app.route('/result')
def do_result():
    selected_val = request.args['selected_val']
    min = request.args['min']
    max = request.args['max']

    val = selected_val.split(",")
    out = get_community(val, min, max)

    return render_template('result.html', scroll='something', out=out)

@app.route('/results')
def do_results():
    selected_val = request.args['selected_val']

    val = selected_val.split(",")
    out = get_community(val)

    return jsonify(out)



@app.route('/description')
def post_history():

    # return a json to see all the variable inputs
    out = "When you are ready to move, we are ready to help. WELCOME TO SFPAL!"
    out = {'description': out}
    return jsonify(out)

@app.route('/map')
def map():
    return render_template('cart.html')


if __name__ == "__main__":
    app.run()# need this to access from the outside world!
