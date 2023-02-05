from outscraper import ApiClient
import requests
import pandas as pd
from flatten_json import flatten


class outscrapper:

    def __init__(self) -> None:
        pass

    def scrapper(self, query, limit, skip=0):
        url = "https://api.app.outscraper.com/maps/search-v2"
        all_query = {
            "query": query,
            "dropDuplicates" : True,
            "skipPlaces": skip,
            "limit": limit,
        }
        headers = {
            "X-API-KEY": "YXV0aDB8NjMzY2YxNjA0YzdhNjRlOTc4NWY3NTZhfDI3OTAwOGEwOWI"
        }

        self.response = requests.get(url, params=all_query, headers=headers).json()
        self.res = requests.get(self.response['results_location'])
        self.result = self.res.json()['data']
    
    # def parameters(data):
    #     if data<200:
    #         skip_place = 0
    #         return data, skip_place
    #     else:
    #         skip_place = int(data/200) * 200 

    def data(self):

        df_final = pd.DataFrame()
        for i,item in enumerate(self.result):
            flattened_query = flatten(item)
            df = pd.DataFrame(data=flattened_query,index=[i])
            df_final = pd.concat([df_final,df],axis=0)
        df_final.reset_index(inplace=True)
