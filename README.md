# SFpal
With SFpal, you can find your next community with ease. 

There are a lot of things to consider for the first time mover to a big city: rent price, commute time, safety, night life, restaurants, outdoor activity, noise, etc. Although you might be able to discover that information from a friend, or a friend’s friend, we merge that data altogether onto one platform to make decisions easier for you. We leverage data to help you decide on an area to live in that caters most to your needs.  


restaurant data :https://data.sfgov.org/Health-and-Social-Services/Restaurant-Scores-LIVES-Standard/pyih-qa8i

Folder development
  - rent_citydata: scarp data from zillow to get rent data and city data from http://www.city-data.com/
    - generate csv file: ZIPdata.csv with all properties, zip.csv with average rent and city data per zip code
    - contians data including: Price, Zillow Price (per sqft), Zillow Rent (per sqft), Income, Poverty (% below the poverty level), Degree (percentage), CostofLiving (living index)
