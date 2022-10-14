# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 12:20:33 2022

@author: prana
"""

from DaytoDaymain import *
from Lastxdaysmain import *
from ageDaytoDaymain import *
from agelastxdaysmain import *
from regionDaytoDaymain import *
from regionlastxdaysmain import *
from actiondevDaytoDay import *
from actiondevLastxdays import *




fields = [
    'account_name',
    'account_id',
    'campaign_id',
    'campaign_name',
    'ad_id',
    'ad_name',
    'adset_id',
    'adset_name',
    'account_currency',
    'spend',
    'impressions',
    'clicks',
    'unique_clicks',
    'conversions',
    'reach',
    'frequency',
    'actions',
    'unique_actions' 
        ]
print('Starting Facebook API...')
print('Type number to select your option:')
print('*******************************')
print("1. Data between two dates.")
print("2. Data for last x amount of days.")
print("3. Data between two dates by age and gender.")
print("4. Data between two dates by region.")
print("5. Data for last x amount of days by age and gender.")
print("6. Data for last x amount of days by region.")
print("7. Data between two dates by action device.")
print("8. Data for last x amount of days by acction device.")
x= int(input("Choose option: "))
Act_id = input('Account Id in the formact act_*********:' )
config_path = input('Path of config file:' )
if x == 1:
   start_date= input('Start date in the format YYYY-MM-DD:' )
   end_date= input('End date in the format YYYY-MM-DD:' )
   DaybyDay(start_date,end_date,Act_id,config_path,fields)
elif x == 2:
    days = input("Number of days you would like to go back: ")
    lastdays(Act_id, days, config_path,fields)
elif x == 3:
   start_date= input('Start date in the format YYYY-MM-DD:' )
   end_date= input('End date in the format YYYY-MM-DD:' )
   ageDaybyDay(start_date,end_date,Act_id,config_path,fields)    
    
elif x == 4:
    start_date= input('Start date in the format YYYY-MM-DD:' )
    end_date= input('End date in the format YYYY-MM-DD:' )
    regionDaybyDay(start_date,end_date,Act_id,config_path,fields) 
elif x == 5: 
    days = input("Number of days you would like to go back: ")
    agelastdays(Act_id, days, config_path,fields) 
elif x == 6: 
    days = input("Number of days you would like to go back: ")
    regionlastdays(Act_id, days, config_path,fields)
elif x == 7: 
    start_date= input('Start date in the format YYYY-MM-DD:' )
    end_date= input('End date in the format YYYY-MM-DD:' )
    actionDaybyDay(start_date,end_date,Act_id,config_path,fields)
elif x ==8:
    days = input("Number of days you would like to go back: ")
    actionlastdays(Act_id, days, config_path,fields)

