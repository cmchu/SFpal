# coding: utf-8
from bs4 import BeautifulSoup
import urllib2
import sys
import csv
import untangle
import re
import pandas as pd

def listToCsv(putListHere): #list is a list of lists [[],[],[],[]]
    with open("ZIPdata.csv", "wb") as data:
        writer = csv.writer(data)
        writer.writerows(putListHere)

# KEY is Zillow key: X1-ZWz19khtiopr0r_4n5nu, X1-ZWz19kgq22gnij_5f91a
def GetZip(city, state, KEY = sys.argv[1]): #given a city and state, returns a list of zip codes from API GetRegionChildren
    ZipList = []
    # Find all zipcode in Seattle
    QuoteURL = "http://www.zillow.com/webservice/GetRegionChildren.htm?zws-id=%s&state=%s&city=%s&childtype=zipcode"

    city = city.replace(' ', '%20')
    state = state.replace(' ', '%20')
    URL = QuoteURL % (KEY, state, city)
    response = urllib2.urlopen(URL)
    xmldata = response.read()  # Seattle read all data

    # Store the zip code in the zipcodelist
    data = untangle.parse(xmldata)

    for zipcode in data.RegionChildren_regionchildren.response.list.region:
        ZipList.append(zipcode.name.cdata)
    return ZipList

def getZPID(property): # Get Property ID given an html and store in a list
    if property.find('a') is None: # if a property has no id
        return 0
    else:
        zpid = property.find('a')['data-fm-zpid']
        return zpid

def getPropertyData(property): # Given the property, get the bath, bed and sqft info
    detail = [x.strip() for x in property.text.split(u'·')]
    for item in detail:
        if item == 'studio': item = 0
    detail = [re.sub("\D", "", x) for x in detail]  # remove char from list, we need number only
    position = [len(detail[0]), len(detail[1]), len(detail[2])].index(max(len(detail[0]), len(detail[1]), len(detail[2])))
    if len(detail[position]) > 2:
        return detail[position]
    else:
        return None
    #return detail[0], detail[1], detail[2], detail[position]


def getRentPrice(zpid, KEY = sys.argv[1]): # Giving a property ID, return the price and rent
    QuoteURL = "http://www.zillow.com/webservice/GetZestimate.htm?zws-id=%s&zpid=%s&rentzestimate=true"
    URL = QuoteURL % (KEY, zpid)
    response = urllib2.urlopen(URL)
    xmldata = response.read()  # Seattle read all data

    # Untangle and get the rent/price for each property
    data = untangle.parse(xmldata)
    try:
        zestimateRent = data.Zestimate_zestimate.response.rentzestimate.amount.cdata
        zestimatePrice = data.Zestimate_zestimate.response.zestimate.amount.cdata
    except:
        zestimatePrice = ""
        zestimateRent = ""
    return zestimatePrice, zestimateRent

def getListPrice(property): # get property price
    if property:
        price = re.sub("\D", "", property.text)
    else:
        price = ''
    return price

def cdScrape(zipCode):
    myurl = urllib2.urlopen("http://www.city-data.com/zips/%s.html" % (zipCode))
    whole = BeautifulSoup(myurl, "html.parser")
    html_text = whole.get_text(' ', strip=False)
    povrate = re.search('(?<=poverty level in 2015:  \n This zip code: )[\d\.]+', html_text)
    mhincome = re.search('(?<=income in 2015:  This zip code: \$)[\d,]{3,}', html_text)
    ageraw = re.search('(?<=resident age: This zip code: )[\d\.]+', html_text)
    ed = re.search("(?<=Bachelor's degree or higher:  )[\d\.]+", html_text)
    costOfLiving = re.search("(?<=living index in zip code [\d]{5}:  )[\d\.]+", html_text)
    metrics = []
    if mhincome:
        income = mhincome.group(0).replace(',', '')
    else:
        income = ''
    if povrate:
        prate = povrate.group(0)
    else:
        prate = ''
    if ageraw:
        age = ageraw.group(0)
    else:
        age = ''
    if ed:
        edd = ed.group(0)
    else:
        edd = ''
    if costOfLiving:
        col = costOfLiving.group(0)
    else:
        col = ''
    return income, prate, edd, col

def HouseGrabber(zip, cityyy, stateee):  #given a zip, returns house stuff
    URL = "http://www.zillow.com/homes/for_sale/94105/house,condo,apartment_duplex,mobile,townhouse_type/1_rs/1_fr/"
    req = urllib2.Request(URL, headers={'User-Agent': 'Resistance Ha'})
    response = urllib2.urlopen(req)
    html = BeautifulSoup(response, "html.parser")

    if html.find_all('h3', {'class': 'zsg-content_collapsed'}):
        pass
    else:
        numResult = html.findAll('meta')[2].attrs[u'content'].split(" ")[2]

    if numResult > 500:
        page = range(20)
    else:
        page = range(int(numResult) / 25)

    ###### DELETE AFTER TESTING #######
    #page = range(1)

    zipdetail = []
    for i in page:
        URL = "http://www.zillow.com/homes/for_sale/%s/house,condo,apartment_duplex,mobile,townhouse_type/%s_p/1_rs/1_fr/" % (zip, i)
        req = urllib2.Request(URL, headers={'User-Agent': 'Resistance Ha'})
        response = urllib2.urlopen(req)
        html = BeautifulSoup(response, "html.parser")

        if html.find_all('h3',{'class':'zsg-content_collapsed'}):       #some ZIPs don't exist, if you search one on zillow it gives "nearby" homes
            pass                                                        #we DON'T want this, therefore if there are no homes it will fail
        else:
            #tempvar1 = citydata()
            #tempvar2 = data2()
            income, prate, edd, col = cdScrape(zip)

            for item in html.find_all(class_="zsg-photo-card-content zsg-aspect-ratio-content"):
                if item.find(class_="zsg-photo-card-actions") is not None:
                    zpid = getZPID(item.find(class_="zsg-photo-card-actions"))
                    if zpid == 0:
                        continue
                    sqft = getPropertyData(item.find(class_="zsg-photo-card-info"))
                    zprice, zrent = getRentPrice(zpid)
                    price = getListPrice (item.find(class_="zsg-photo-card-price"))

                    zipdetail.append((cityyy, stateee, zip, zpid, sqft, price, zprice, zrent, income, prate, edd, col))

    return zipdetail

def getEverything():
    fulllist = [['City', 'State', 'ZIP', 'ZillowID','sqft', 'Price', 'ZPrice', 'ZRent', 'Income', 'Poverty','Degree', 'CostofLiving']]    #citylist = getCitylist()
    citylist = [['San Francisco','CA']]
    for city in citylist:
        ziplist = GetZip(city[0], city[1])
        for zip in ziplist[0:3]:
           fulllist.extend(HouseGrabber(zip, city[0], city[1]))
    return fulllist

# Get all properties for all zipcode
table = getEverything()
listToCsv(table)

# Get average rent, price per zipcode
headers = table.pop(0)
df = pd.DataFrame(table, columns=headers)
for c in ['sqft','Price', 'ZPrice', 'ZRent', 'Income', 'Poverty','Degree', 'CostofLiving']:
    df[c] = pd.to_numeric(df[c])
df['RentSqft'] = df['ZRent']/df['sqft']
dfgroup = df.groupby(['City', 'State', 'ZIP'], axis=0)['Price', 'ZPrice', 'ZRent', 'RentSqft','Income', 'Poverty','Degree', 'CostofLiving'].mean()

dfgroup.to_csv('zip.csv')