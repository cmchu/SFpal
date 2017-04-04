# SFpal
With SFpal, you can find your next community with ease. 

There are many factors to consider for an individual moving to a big city: rent price, commute time, safety, nightlife, restaurants, outdoor activities, noise, etc. Although you might be able to discover that information from a friend (or a friend’s friend) we merge that data altogether onto one platform to make decisions easier for you. We leverage data to help you decide on an area to live in that caters most to your needs. 

## Community Definition
San Francisco can be divided into many different communities, such as based on demographics, physical boundaries, main streets, etc. The sizes of these communities can vary greatly. We desired community delineations that resulted in areas not too large (so that our app will actually have value to the user), but also areas not too small (so that the user will be able to find available housing). The two main community divisions we examined were zipcode and zoning district. We chose to use zipcode as the community definition because we felt that the zoning districts were too small and, thus, restrictive. However, we are open to changing this definition and have written the code to allow for this.

Zipcode data was subsetted to only those in San Francisco and was collected from the following source:
https://data.sfgov.org/Geographic-Locations-and-Boundaries/Bay-Area-ZIP-Codes/u5j3-svi6/data

## Data Collection
One of the important aspects of this app is collecting accurate data on all different aspects of living. The following is a list of the types of data we collected and their source in no particular order:
  - restaurant data
    - https://data.sfgov.org/Health-and-Social-Services/Restaurant-Scores-LIVES-Standard/pyih-qa8i
  - parks data
    - https://data.sfgov.org/Culture-and-Recreation/Park-and-Open-Space-Map/4udc-s3pr
  - schools data
    - https://data.sfgov.org/Economy-and-Community/Schools/tpp3-epx2
  - bart stations data
    - http://www.dot.ca.gov/hq/tsip/gis/datalibrary/Metadata/BART_13.html

After collection of all data, we spatially joined the data with the zipcode data in order to be able to analyze all data by zipcode and in order to make sure all zipcode definitions are equivalent.

## Community Recommendation System

## Visualizations

## App Architecture
For app development, we used Python Flask.

## Folder description
### data
This folder contains two sub-folders: raw_data and clean_data.
  - **clean_data** contains the data from the **raw_data** folder after being cleaned and spatially joined with the zipcode data.

### development
This folder contains code to gather/scrape data, clean data, and spatially analyze data.
  - rent_citydata.py
    - scrapes data from Zillow and City-Data
    - gathers data on Price, Zillow Price (per sqft), Zillow Rent (per sqft), Income, Poverty (% below the poverty level), Degree (percentage who have Bachelor's degree), Cost of Living (living index)
    - generates ZIPdata.csv file and zip.csv file
      - ZIPdata.csv contains data on every listing in San Francisco
      - zip.csv condenses the data in ZIPdata.csv to provide averaged data for each zip code
  - GeoData_Analysis.ipynb
    - cleans parks, schools, and bart stations data, and spatially joins them with zipcode data
    - reads in data from raw_data folder
    - generates cleaned csv files, which are placed into the clean_data folder

### functions 
This folder contains sub-folders: app,data cleaning, data transforming, and data scraping.
  - **app** contains app architecture (server, client, etc.).

  
## Python Package Dependencies
  - geopandas
    - to install with Anaconda: 
      - conda install -c conda-forge geopandas
