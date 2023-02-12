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
                return result["data"]
            else:
                time.sleep(30)
                continue


    def data(self,result):

        df_final = pd.DataFrame()
        for i,item in enumerate(result):
            flattened_query = flatten(item)
            df = pd.DataFrame(data=flattened_query,index=[i])
            df_final = pd.concat([df_final,df],axis=0)

        return df_final

    def processInput(self,lines):
        print("Wait, we are fetching data for you...")
        i=0
        merged = pd.DataFrame()
        for line in lines[1:]:
            cols = line.split(',')
            zip_code = cols[0]
            area = cols[1]
            limit = int(cols[2]) 
            businesses = cols[3:]

            final = pd.DataFrame()
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
                final_res = self.data(dict_response)
                final = pd.concat([final,final_res],axis=0)
            final.reset_index(inplace=True)
            final = final.drop_duplicates()
            if not os.path.exists("./output"):
                os.makedirs("./output")
            if not os.path.exists("./output/"+str(today)):
                os.makedirs("./output/"+str(today))
            final.to_csv("output/"+str(today)+"/"+str(zip_code)+".csv")
            i=i+1
            print(str(i)+ " csv file saved !!")
            merged = pd.concat([merged,final],axis=0)
        merged.reset_index(inplace=True)
        merged.to_csv("./output/"+str(today)+"/"+"merged.csv")
        print("Merged csv saved !!")
        
        
