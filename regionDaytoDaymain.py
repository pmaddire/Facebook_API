# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 15:57:54 2022

@author: prana
"""
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from datetime import timedelta, date
import pandas as pd
import os
from configparser import ConfigParser
import psycopg2
import sys
from fields import *

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def regionDaybyDay(start_date,end_date,account_id,config_path,fieldf):

    print('starting...')
    
    #open config file
    configur = ConfigParser()
    configur.read(config_path)
    #os_username = os.environ.get('USERNAME') #finding enviromental variable 'user' 
    path = configur.get('address','path')
    #path = path.replace('"','')
    my_path = path+"region"+"/"+account_id 
    
    #set up new directory
    try:
        os.makedirs(my_path,exist_ok=True)
    except OSError as error : #dodge directory already exists error
        t=1
    
    #function to help iterate between two dates

    
    
    
    #turning user inputed dates into date type values
    days_in_month = []
    d_1 = int(start_date[8:10])
    d_2 = int(end_date[8:10])
    m_1 = int(start_date[5:7])
    m_2 = int(end_date[5:7])
    year_1 = int(start_date[0:4])
    year_2 = int(end_date[0:4])
    #print(d_1)
    #print(m_1)
    
    start_date = date(year_1,m_1,d_1)
    end_date = date(year_2,m_2,d_2+1)
    
    #setup for API call
    app_id = configur.get('api','app_id')
    app_secret = configur.get('api','app_secret')
    access_token = configur.get('api','access_token')
    
    FacebookAdsApi.init(app_id, app_secret, access_token)
    
    
    #API calls for each day from start date to end date for each campaign id
    for single_date in daterange(start_date, end_date):
        day_d=(single_date.strftime("%Y-%m-%d"))
        #API call to find all campaigns in an account
        params = {
                'level': 'campaign',
                'time_range':{'since': day_d,'until':day_d,
                     
                              },
                #'time_increment': 1,
                #'date_preset': 'last_7d' 
                }
    
        fields = [
                'campaign_id',
                'campaign_name',
    
    
                ]
    
        insights = AdAccount(account_id).get_insights(
                params = params,
                fields = fields,
                )
    
        index = 0
        campaign_id_list =[] #empty list for campaign ids
        results = []         #empty list for insights data
    
        #prepare data for data frame
        for i in insights:
            data = dict(i)
            results.append(data)
        #print(results)
        length = len(results)
        df= pd.DataFrame(results) #insert insight data into a data frame (table)
    
        #read campaign ids from table and put them into campaign_id_list
        for i in range(length):
            l = df.at[i,'campaign_id']
            campaign_id_list.append(l)
               
    
        for cid in campaign_id_list:
            my_path_d = my_path+"/"+day_d
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
                'limit':10000,
                
                'level': 'ad',
                'time_range':{'since': day_d,'until':day_d,
                     
                              },
                'action_attribution_windows': ['1d_click','1d_view','7d_view','7d_click','28d_click','28d_view'],
                'breakdowns':[
                    'region',
               
                    ]
                   
                }
                #'time_increment': 1,
                #'date_preset': 'last_7d' }
    
            fields = fieldf
    
            insights = AdAccount(account_id).get_insights(
                params = params,
                fields = fields,
                )
            #formatting json
            length = len(insights)
            for i in range(0,length):
                instring = str(insights[i])
                
                instring = instring.replace('<AdsInsights>', '').replace("\r",'').replace('\n','').replace(' ','')
                #writing data to file
                f.write(instring)
                f.write('\n')
                
            

            print("printing...")                
            #f.write(str(insights[0]))
            f.close()
 

start_date = sys.argv[1] #start date
end_date = sys.argv[2] #end date
account_id = sys.argv[3] #account_id
config_path = sys.argv[4] #config file path
fieldf = feildsAPI()
account_id = 'act_'+str(account_id)
regionDaybyDay(start_date,end_date,account_id,config_path,fieldf)




