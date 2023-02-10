
# Automation

We are automation the outscraper api call with different criteria


## Documentation

## Input: 
We are using a text file as input which will contain 3 information

#### Look like this

| Zip code | Business type     | Number of response need                       |
| :-------- | :------- | :-------------------------------- |
| `integer`      | `string` |  integer |

#### Process of API calss
we are using outscrapper api for pulling data
```http
  GET https://api.app.outscraper.com/maps/search-v2
```
query pattern
```
  query = {
      "query": "restaurants, Manhattan, NY, USA",
      "dropDuplicates" : True,
      "limit": 200,
  }
```
#### Step 1
now we are we have developed a function which will call api for each Zip code and with different Business criteria.

#### Step 2
after getting the api response for each Zip code we making dataframe, Dropping the duplicates and finally we are merging all response for each zip. And saving dataframe as sheet
```
df.to_csv("data.csv",index=False)
```

#### Step 3
after this we are making another sheet for Useartemis with only those columns which are required for bulk searching
