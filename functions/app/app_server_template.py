from flask import Flask, request, jsonify,render_template, redirect

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def default():

    #output = dict()

    # this could be a web page of docs instead
    #output['message'] = 'Welcome to the SFpal!'
    if request.method == "POST":
        if request.form['submit'] == 'submit':
            selected = request.form.getlist('check')
            any_selected = bool(selected)
            print selected
    return render_template('mainpage.html')
    #return script
   
@app.route('/Ready')
def post_history():

    #return a json to see all the variable inputs
    out = request.args.to_dict()

    return jsonify(out)

@app.route('/result',methods = ['POST', 'GET'])
def result():

    test = request.form.getlist('checks')
    print test
    return jsonify(test)
   #else:
    #   return redirect('/')

@app.route('/test2', methods=['GET', 'POST'])
def test2():

    if request.method == "POST":
        if request.form['submit'] == 'submit':
            print(request.args.get('check'))

    return render_template('test.html')


if __name__ == "__main__":
    app.debug = True # only have this on for debugging!
    app.run(host='0.0.0.0') # need this to access from the outside world!
