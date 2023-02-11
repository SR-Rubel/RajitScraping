import requests
import pandas as pd
from flatten_json import flatten


class outscrapperHelper:

    def __init__(self) -> None:
        pass

    def scrapper(self, query):
        url = "https://api.app.outscraper.com/maps/search-v2"
        headers = {
            "X-API-KEY": "YXV0aDB8NjMzY2YxNjA0YzdhNjRlOTc4NWY3NTZhfDI3OTAwOGEwOWI"
        }

        self.response = requests.get(url, params=query, headers=headers).json()
        self.res = requests.get(self.response['results_location'])
        result = self.res.json()['data']
        return result
    
    # def parameters(data):
    #     if data<200:
    #         skip_place = 0
    #         return data, skip_place
    #     else:
    #         skip_place = int(data/200) * 200 

    def data(self,result):

        df_final = pd.DataFrame()
        for i,item in enumerate(result):
            flattened_query = flatten(item)
            df = pd.DataFrame(data=flattened_query,index=[i])
            df_final = pd.concat([df_final,df],axis=0)
        return df_final.reset_index(inplace=True)

    def processInput(self,lines):
        req_query = {
            "query": [],
            "dropDuplicates" : True,
            "skipPlaces": 0,
            "limit": [],
        }
        inputs = []
        for line in lines:
            cols = line.split(',')
            limit = cols[0]
            zip_code = cols[1]
            businesses = cols[2:-1]
            req_query['query'].append(businesses)
            req_query['limit'].append(limit)
    # def processInput(self,lines):
    #     inputs = []
    #     for line in lines:
    #         cols = line.split(',')
    #         limit = cols[0]
    #         zip_code = cols[1]
    #         businesses = cols[2:-1]
    #         for business in businesses:
    #             req_query = {
    #                 'query': (str(zip_code)+' '+str(business)).strip(),
    #                 'limit': limit,
    #                 "dropDuplicates" : True,
    #                 "skipPlaces": 0,
    #             }
    #             inputs.append(req_query)
    #     return inputs
    def processInput(self,lines):
        inputs = []
        for line in lines:
            cols = line.split(',')
            limit = cols[0]
            zip_code = cols[1]
            businesses = cols[2:-1]
            for business in businesses:
                req_query = {
                    'query': (str(zip_code)+' '+str(business)).strip(),
                    'limit': limit,
                    "dropDuplicates" : True,
                    "skipPlaces": 0,
                    'name':str(zip_code)
                }
                inputs.append(req_query)
        return inputs
