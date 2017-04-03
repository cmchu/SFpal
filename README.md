# SFpal
With SFpal, you can find your next community with ease. 

There are many factors to consider for an individual moving to a big city: rent price, commute time, safety, nightlife, restaurants, outdoor activities, noise, etc. Although you might be able to discover that information from a friend (or a friend’s friend) we merge that data altogether onto one platform to make decisions easier for you. We leverage data to help you decide on an area to live in that caters most to your needs. 


restaurant data: https://data.sfgov.org/Health-and-Social-Services/Restaurant-Scores-LIVES-Standard/pyih-qa8i

parks data: https://data.sfgov.org/Culture-and-Recreation/Park-and-Open-Space-Map/4udc-s3pr

schools data: https://data.sfgov.org/Economy-and-Community/Schools/tpp3-epx2

zipcode data: https://data.sfgov.org/Geographic-Locations-and-Boundaries/Bay-Area-ZIP-Codes/u5j3-svi6/data

bart data: https://www.bart.gov/schedules/developers/geo ; http://www.dot.ca.gov/hq/tsip/gis/datalibrary/Metadata/BART_13.html

## Folder description
### development
  - rent_citydata: scrape data from zillow to get rent data and city data from http://www.city-data.com/
    - generate csv file: ZIPdata.csv with all properties, zip.csv with average rent and city data per zip code
    - contians data including: Price, Zillow Price (per sqft), Zillow Rent (per sqft), Income, Poverty (% below the poverty level), Degree (percentage), CostofLiving (living index)

  
## Python Package Dependencies
  - geopandas
    - to install with Anaconda: 
      - conda install -c conda-forge geopandas
