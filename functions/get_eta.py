import simplejson, urllib

def get_time_sec(orig_coord,dest_coord,API_KEY,mode ='transit'):
	'''
	param orig_coord(str) "32.32,20.30" 
	param dest_coord(str) "32.32,20.30"
	param API_KEY(str) google api
	param mode(str) options: 'driving','walking','transit','bicycling'
	return integer(in second)
	'''
	url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={0}&destinations={1}&mode={2}&key={3}'.format(orig_coord,dest_coord,mode,API_KEY)
	
	result= simplejson.load(urllib.urlopen(url))
	
	return result['rows'][0]['elements'][0]['duration']['value']
