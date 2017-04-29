import simplejson, urllib
import pandas as pd
import shapefile
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname("get_eta"), '..', 'functions/data_transforming')))

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


def batch_time(orig_coord,API_KEY,is_driving=False):

    reader= shapefile.Reader('../data/clean_data/SF_zip_points/point.shp')
    df = pd.DataFrame(columns=['zip','lon','lat'])
    fields = [field[0] for field in reader.fields[1:]]
    for i,feature in enumerate(reader.shapeRecords()):
        geom = feature.shape.__geo_interface__
        atr = dict(zip(fields, feature.record))
        result = pd.DataFrame({'zip':str(int(atr['ID'])),'lon':geom['coordinates'][0],'lat':geom['coordinates'][1]},index=[i])
        df =df.append(result)
    df['coords']= df[['lon', 'lat']].apply(lambda x: ','.join(x.fillna('').map(str)), axis=1)
    if not is_driving:
        df['transit']= df['coords'].apply(lambda x: get_time_sec(orig_coord,x,API_KEY,'transit'))
        df['walking']= df['coords'].apply(lambda x: get_time_sec(orig_coord,x,API_KEY,'walking'))
        df['mindist'] = df[['transit','walking']].min(axis=1)
    else:
        df['mindist']= df['coords'].apply(lambda x: get_time_sec(orig_coord,x,config_appdev.API_KEY,'driving'))
        
    return df.groupby('zip').mindist.mean()
        


            
        
    
    
    
    
