from flask import Flask, request, jsonify,render_template, redirect, url_for

app = Flask(__name__)


def predict(input):
    from sklearn.metrics import jaccard_similarity_score
    import pandas as pd
    gold_standard = pd.read_csv('gold_standard.csv')
    for row in range(gold_standard.shape[0]):
        similarity = jaccard_similarity_score(gold_standard.drop(["similarity", "zip"], axis=1).ix[row,],input)
        gold_standard.ix[row, "similarity"] = similarity

    return gold_standard.sort_values("similarity", ascending=False).reset_index(drop=True).ix[[0, 1, 2], "zip"]


def get_community(selected, min, max):

    keys = ["sanitation", "peace_quiet", "appearance", "children_friendly", "walking_condition", "coffee", "nightlife", "dog_friendly", "construction", "parks", "schools", "bart_stations", "safety", "restaurants"]
    vals = [1.0 if i in selected else 0.0 for i in keys]
    vals.append([int(min), int(max)])
    print vals
    prediction = predict(vals)
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
