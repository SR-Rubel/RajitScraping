import requests
import pandas as pd
from flatten_json import flatten
from datetime import date
import os
from outscraper import ApiClient
import time


today = date.today()

class outscrapperHelper:

    def __init__(self) -> None:
        self.client = ApiClient(api_key='YXV0aDB8NjMzY2YxNjA0YzdhNjRlOTc4NWY3NTZhfDI3OTAwOGEwOWI')

    def scrapper(self, query):
        url = "https://api.app.outscraper.com/maps/search-v2"
        headers = {
            "X-API-KEY": "YXV0aDB8NjMzY2YxNjA0YzdhNjRlOTc4NWY3NTZhfDI3OTAwOGEwOWI"
        }
        for i in range(5):
            response_data = requests.get(url, params=query, headers=headers)
            response_data = response_data.json()
            response_id = str(response_data["id"])
            result = self.client.get_request_archive(response_id)
            if(result["status"]=="Success"):
                # print(result["data"])
                return result["data"]
            else:
                time.sleep(30)
                continue
        # response_data = response_data.json()
        # print(response_data)
        # response_data = response_data["results_location"]
        # res = requests.get(response_data)
        # result = res.json()
        # print(result.keys())
        # if("data" not in result.keys()):
        #     return {}
        # else:
        # print(result)
        # result = result["data"]
        # return result
    
    # def parameters(data):
    #     if data<200:
    #         skip_place = 0
    #         return data, skip_place
    #     else:
    #         skip_place = int(data/200) * 200 

    def data(self,result):

        df_final = pd.DataFrame()
        for i,item in enumerate(result):
            # print(result)
            flattened_query = flatten(item)
            df = pd.DataFrame(data=flattened_query,index=[i])
            df_final = pd.concat([df_final,df],axis=0)
            # print(df_final)
        return df_final.reset_index(inplace=True)

    # def processInput(self,lines):
    #     req_query = {
    #         "query": [],
    #         "dropDuplicates" : True,
    #         "skipPlaces": 0,
    #         "limit": [],
    #     }
    #     inputs = []
    #     for line in lines:
    #         cols = line.split(',')
    #         limit = cols[0]
    #         zip_code = cols[1]
    #         businesses = cols[2:-1]
    #         req_query['query'].append(businesses)
    #         req_query['limit'].append(limit)
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
        for line in lines[1:]:
            cols = line.split(',')
            # print(cols)
            zip_code = cols[0]
            area = cols[1]
            limit = int(cols[2]) 
            businesses = cols[3:]
            print(businesses)

            final_df = pd.DataFrame()
            for business in businesses:
                business = str(business)
                business.replace("\n",'')
                business.strip()
                req_query = {
                    'query': (str(zip_code).strip()+' '+str(area).strip()+' '+str(business).strip()).strip(),
                    'limit': limit,
                    "dropDuplicates" : True,
                    "skipPlaces": 0,
                    "async": False
                }
                dict_response = self.scrapper(req_query)
                # print(dict_response)
                final_res = self.data(dict_response)
                print(final_res)
                final_df = pd.concat([final_df,final_res],axis=0)
                final_df.reset_index(inplace=True)
                # print(final_df)
                final_df = final_df.drop_duplicates()
                if not os.path.exists("./output"):
                    os.makedirs("./output")
                if not os.path.exists("./output/"+str(today)):
                    os.makedirs("./output/"+str(today))
                final_df.to_csv("output/"+str(today)+"/"+str(zip_code)+".csv")
        
