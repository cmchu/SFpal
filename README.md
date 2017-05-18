# SFpal
Contributors: Christine Chu, Tianyi Liu, Evelyn Peng

Visit [sfpal.life](sfpal.life)

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
  - SF Police Department Incidents data
    - https://data.sfgov.org/Public-Safety/SFPD-Incidents-from-1-January-2003/tmnf-yvry/data
  - SF Police Department Locations data
    - https://data.sfgov.org/Public-Safety/Police-Stations-2011-/rwdu-9wb2
  - rent, house price data
    - https://www.zillow.com/
  - city data
    - http://www.city-data.com/
     

After collection of all data, we spatially joined the data with the zipcode data in order to be able to analyze all data by zipcode and in order to make sure all zipcode definitions are equivalent.

## Community Recommendation System
Since the app is in its development phase, we are dealing with the cold start problem. This means we do not have any prior data about user behavior. Therefore, our unique solution to this problem was to create a gold standard, based on both the above collected data and our personal feelings. To do this, we traveled to every community and recorded our feelings in predetermined categories (i.e., safety, appearance, etc). Finally, in order to recommend a community to a user, we calculated the Jaccard similarity between the users preferences and the gold standard we created for each community. The community with the highest similarity to the users preferences is the top recommended community.

In the future, we plan to get feedback from our users about how well our recommendation system performed. Using that data, we then plan to create a more robust recommendation system.

## Visualizations
We used CartoDB in order to show on a map the location of the top recommended community.

## App Architecture
For app development, we used Python Flask.

## Folder description
### data
This folder contains two sub-folders: raw_data and clean_data.
  - **clean_data** contains the data from the **raw_data** folder after being cleaned and spatially joined with the zipcode data.
  - **raw_data** contains the originally scraped data or downloaded data

### development
This folder contains code written in the development phase to gather/scrape data, clean data, and spatially analyze data. These files were then incorporated into our final app.

### functions 
This folder contains sub-folders: app, data cleaning, data transforming, and data scraping.
  - **app** contains the app architecture (server, client, etc.).
  - **data_scraping** contains the code used to scrape data from Zillow and City-Data.
  - **data transforming** contains code to get the estimated time from one zip code to a specified address.
  
## Python Package Dependencies
  - geopandas
    - to install with Anaconda: 
      - conda install -c conda-forge geopandas
  - BeautifulSoup
  - urllib2
  - untangle
