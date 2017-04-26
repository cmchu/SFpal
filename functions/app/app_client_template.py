import httplib
from bs4 import BeautifulSoup
import urllib2

# project name: SFpal

# authors are Christine Chu, Linda Liu, Evelyn Peng


# use this server for dev
SERVER = 'ec2-54-186-133-112.us-west-2.compute.amazonaws.com/'

# use this server for prod, once it's on ec2
# SERVER = 'xxxxx.aws.ec2.com:5000'
def get_default():

    URL = 'http://'+SERVER+''
    print URL
    req = urllib2.Request(URL, headers={'User-Agent2': "Resistance is futile"})
    out = urllib2.urlopen(req)

    return out.read()

def get_result():
    keys = ["sanitation", 'coffee', "construction"]
    URL = 'http://'+SERVER+'/result?selected_val=' + "%2C".join(keys)+'#something'
    req = urllib2.Request(URL, headers={'User-Agent': "Resistance is futile"})
    out = urllib2.urlopen(req)
    soup = BeautifulSoup(out, 'html.parser')
    result = soup.find("section", {"id": "services"})

    return result.table


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