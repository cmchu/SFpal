import geopandas as gpd
from shapely.geometry import Point

def spatial_join_zipcode(df, communities):
    """
    Function to spatially join communities data to a dataframe with latitude and longitude.
    Note: "lat_long" column must be of tuple type with first element being latitude
          and second element being longitude

    df: pandas dataframe with "lat_long" column
    communities: geopandas dataframe with polygon geometry
    """
    df["geometry"] = df["lat_long"].apply(lambda x: Point(tuple(reversed(eval(x)))))
    if hasattr(df, 'crs'):
        df = df.to_crs(communities.crs)
    else:
        df.crs = communities.crs
    df = gpd.sjoin(df, communities, how="inner", op='intersects')
    del df["index_right"]

    return df