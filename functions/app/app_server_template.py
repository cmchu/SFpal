from flask import Flask, request, jsonify,render_template


app = Flask(__name__)


@app.route('/')
def default():

    #output = dict()

    # this could be a web page of docs instead
    #output['message'] = 'Welcome to the SFpal!'
    return render_template('mainpage.html')
    #return script
   
@app.route('/Ready')
def post_history():

    #return a json to see all the variable inputs
    out = request.args.to_dict()

    return jsonify(out)

if __name__ == "__main__":
    app.debug = True # only have this on for debugging!
    app.run(host='0.0.0.0') # need this to access from the outside world!
