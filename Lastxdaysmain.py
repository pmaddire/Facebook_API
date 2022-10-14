# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 15:14:03 2022

@author: prana
"""


from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from datetime import timedelta, date
import pandas as pd
import os
from configparser import ConfigParser
import sys
from fields import *



def daterange(start_date, end_date):   #function that helps iterate through dates
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def lastdays(account_id, days, config_path,fieldf):
   
    #open config file 
    configur = ConfigParser()
    configur.read(config_path)
    print('starting...')
    #os_username = os.environ.get('USERNAME')  #find enviromental variable "User"
    path = configur.get('address','path') 
    my_path = path+"insights"+"/"+account_id #setting directory in user
    try:
        os.makedirs(my_path,exist_ok=True) #creating directory
    except OSError as error :              #dodgeing error if directory already exists
        t=1
    

    
    end_date = date.today() #setting the last date of query to today
    end_date = end_date + timedelta(days=1) #change to include today in API calls
    start_date = end_date - timedelta(days=int(days))   #Setting start date to user inputed days ago
    
    # setup for API call
    #setup for API call
    app_id = configur.get('api','app_id')
    app_secret = configur.get('api','app_secret')
    access_token = configur.get('api','access_token')
    
    
    FacebookAdsApi.init(app_id, app_secret, access_token)
    
    
    
    #API calls for all campaigns by date for the last x days
    #data is stored in seperate folders for each day and separated in different files for each campaign
    for single_date in daterange(start_date, end_date):
        day_d=(single_date.strftime("%Y-%m-%d"))
        #Call to find Campaign ids within an account
        params = {
                'level': 'campaign',
                'time_range':{'since': str(start_date),'until':str(end_date),
                     
                              },
    
                }
    
        fields = [
                'campaign_id',
                'campaign_name',
    
    
                ]
    
        insights = AdAccount(account_id).get_insights(
                params = params,
                fields = fields,
                )
    
    
        campaign_id_list =[] #empty list for ids
        results = []         #empty list for index
    
        #preparing insights in list results to be inputed into a data frame
        for i in insights:
            data = dict(i)
            results.append(data)
    
        length = len(results)
        df= pd.DataFrame(results)  #turn insights into a table to make pulling campaign ids easy
    
        #pulling campiagn ids from data frame
        for i in range(length):
            l = df.at[i,'campaign_id']
            campaign_id_list.append(l)
        #print(campaign_id_list)
        for cid in campaign_id_list:
            my_path_d = my_path + "/"+day_d
            try:
                os.makedirs(my_path_d,exist_ok=True)
            except OSError as error :
                t=1
            name = "/"+ day_d+"-"+account_id+"-"+cid+".json"
            f = open(my_path_d+name, 'w')
            params = {
                'filtering' : [
                        {
                            'field' : 'campaign.id',
                            'operator'  : 'EQUAL',
                            'value' : cid, 
                            },
                    
                    ],
                
                'level': 'ad',
                'time_range':{'since': day_d,'until':day_d,
                              }, 
                'action_attribution_windows': ['1d_click','1d_view','7d_view','7d_click','28d_click','28d_view']
                    }
    #action_attribution_windows=1d_click,1d_view,7d_view,7d_click,28d_click,28d_view
            fields = fieldf
    
            insights = AdAccount(account_id).get_insights(
                params = params,
                fields = fields,
                )
            #Formating for json
            instring = str(insights)
            length = len(insights)
            for i in range(0,length):
                instring = str(insights[i])
                instring = instring.replace('<AdsInsights>', '').replace("\r",'').replace('\n','').replace(' ','')
                #writing data to file
                f.write(instring)
                f.write('\n')
                
                    
           # f.write(str(instring))
            print('printing...')
            f.close()
    print("done")

days = sys.argv[1]
account_id = sys.argv[2]
config_path = sys.argv[3]
account_id = 'act_'+str(account_id)
fieldf = feildsAPI()
lastdays(account_id, days, config_path,fieldf)