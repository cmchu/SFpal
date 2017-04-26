import httplib
from bs4 import BeautifulSoup


# project name: SFpal

# authors are Christine Chu, Linda Liu, Evelyn Peng


# use this server for dev
SERVER = '0.0.0.0:5000'

# use this server for prod, once it's on ec2
# SERVER = 'xxxxx.aws.ec2.com:5000'
def get_default():
    out = dict()
    h = httplib.HTTPConnection(SERVER)
    h.request('GET', 'http://'+SERVER+'/description')
    resp = h.getresponse()
    out = resp.read()
    return out

def get_result():
    keys = ["sanitation", 'coffee', "construction"]

    h = httplib.HTTPConnection(SERVER)

    # want the url to look like this
    # http://0.0.0.0:5000/result?selected_val=sanitation%2Ccoffee%2Cconstruction#something
    h.request('GET', 'http://'+SERVER+'/results?selected_val=' + "%2C".join(keys)+ 'type=json'+'#something')
    resp = h.getresponse()
    out = resp.read()
    return out

    # soup = BeautifulSoup(out, 'html.parser')
    # result = soup.find("section", {"id": "services"})
    #
    # return result.table


if __name__ == '__main__':
    print "************************************************"
    print "test of my flask app running at ", SERVER
    print "created by  Christine Chu, Linda Liu, Evelyn Peng"
    print "************************************************"
    print "******** SFpal class test **********"
    print "Here we enter three things that we want our" \
          " community to look like: 'sanitation', 'coffee', 'construction'"
    print "The app will deliver three zipcodes that best meet our requirement:"
    print get_result()
    print "************************************************"
    print "******** SFpal default **********"
    print get_default()