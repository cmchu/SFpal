from flask import Flask, request, jsonify,render_template


app = Flask(__name__)


@app.route('/')
def default():

    #output = dict()

    # this could be a web page of docs instead
    #output['message'] = 'Welcome to the SFpal!'
    return render_template('mainpage.html')
    #return script


@app.route('/resource')
def get_resource():
    """

    """

    out = dict()

    out['result'] = 'This is the resource'

    return jsonify(out)


@app.route('/resource/<var>')
def get_resource_var(var):
    """
    """
    user = request.args.get('user')
    out = dict()
    if user:
        out['user'] = user
    out['var'] = var

    return jsonify(out)

if __name__ == "__main__":
    app.debug = True # only have this on for debugging!
    app.run(host='0.0.0.0') # need this to access from the outside world!
