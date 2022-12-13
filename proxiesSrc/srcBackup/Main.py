'''

All work by Darien Nouri


'''
import csv
from bs4.element import SoupStrainer
from sqlalchemy import create_engine
import urllib
import pyodbc
import pandas as pd
import sqlalchemy
import time
import sys
import numpy as np
import pandas as pd
import tkinter as tk
import requests
import urllib3
import json
import html
import requests
from openpyxl import Workbook
import argparse
from csv import writer
import os
from bs4 import BeautifulSoup
import tkinter as tk
import requests
from sqlalchemy import create_engine
import urllib
from datetime import datetime
from sqlalchemy import create_engine
import urllib
import xlsxwriter
from datetime import datetime
pd.options.mode.chained_assignment = None  # default='warn'
from Zillow import Zillow
import traceback #git checkout -b 12_11CompileUpdatePush origin/compileSave_ScraperAPI
import concurrent.futures
import csv
import urllib.parse



def main(input_url, starting_price = 1000):
    
    
    zillow = Zillow()
    zillow.starting_price = zillow.current_price = starting_price 
    zillow.previous_price = 0
    zillow.parseInputUrl(input_url)
    zillow.updateUrlPrice(zillow.current_price, first_run=True)
    rounds = 0
    try:
        while zillow.current_price > starting_price-1: 
            rounds+=1
            print()
            print('Price Reset')
            if rounds > 1: zillow.updateUrlPrice(zillow.current_price)                    
                                
            for page_num in range(1,9):
                zillow.updateUrlPage(page_num)
                
                listing_links = zillow.getListingLinks()
                if listing_links is None:
                    continue
                zillow.async_count = 0
                
                import logging
                try:
                    zillow.download_many1(listing_links)
                except concurrent.futures._base.TimeoutError:
                    logging.info('timeout!')
                finally:
                    logging.info('2 finished\n')
            
                #zillow.runAsync(listing_links)
                
                #zillow.previous_price = zillow.current_price

                if len(zillow.listingDatabase) > 1 and len(zillow.listingDatabase) < 41:
                    zillow.getSaveName()
                if len(zillow.listingDatabase) > 5 and zillow.current_price < (zillow.listingDatabase[-4]['price']):     
                    zillow.exitProgram()

                #elif zillow.current_price < (starting_price-1):                  
                #    zillow.exitProgram()#git push –set-upstream origin FastScraperAPI
                if page_num % 4:
                    zillow.saveCSV()
                    zillow.create_excel()
                print(len(zillow.listingDatabase),zillow.current_price)       
        else:
            print('Done Scraping', len(zillow.listingDatabase), 'Listings!')
            return zillow.listingDatabase
    except Exception:
        print(traceback.format_exc())
    #except Exception:
        #zillow.saveCSV()
        ##zillow.create_excel()  
        #print(traceback.format_exc())
        print("")
    #    zillow.exitProgram()
          
if __name__ ==  "__main__":

    test_link = 'https://www.zillow.com/new-york-ny/2_p/?searchQueryState=%7B%22pagination%22%3A%7B%22currentPage%22%3A2%7D%2C%22usersSearchTerm%22%3A%22New%20York%2C%20NY%22%2C%22mapBounds%22%3A%7B%22west%22%3A-74.49741171289062%2C%22east%22%3A-73.46195028710937%2C%22south%22%3A40.35337908958887%2C%22north%22%3A41.04055196752766%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A6181%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22min%22%3A20000000%7D%2C%22mp%22%3A%7B%22min%22%3A94994%7D%2C%22sort%22%3A%7B%22value%22%3A%22pricea%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%7D'
    
    links = {

    'NY':'https://www.zillow.com/ny/2_p/?searchQueryState=%7B%22pagination%22%3A%7B%22currentPage%22%3A2%7D%2C%22usersSearchTerm%22%3A%22NY%22%2C%22mapBounds%22%3A%7B%22west%22%3A-79.911886203125%2C%22east%22%3A-71.628194796875%2C%22south%22%3A40.07057084687667%2C%22north%22%3A45.391566871346015%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A43%2C%22regionType%22%3A2%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22min%22%3A300000%7D%2C%22mp%22%3A%7B%22min%22%3A1436%7D%2C%22sort%22%3A%7B%22value%22%3A%22pricea%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A7%7D',
    'NJ':'https://www.zillow.com/nj/2_p/?searchQueryState=%7B%22pagination%22%3A%7B%22currentPage%22%3A2%7D%2C%22usersSearchTerm%22%3A%22NJ%22%2C%22mapBounds%22%3A%7B%22west%22%3A-76.7952458515625%2C%22east%22%3A-72.6534001484375%2C%22south%22%3A38.68416008936318%2C%22north%22%3A41.45789958695567%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A40%2C%22regionType%22%3A2%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22mp%22%3A%7B%22min%22%3A1436%7D%2C%22sort%22%3A%7B%22value%22%3A%22pricea%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22price%22%3A%7B%22min%22%3A300000%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A8%7D'

    }
    
    print("Starting...")
    
    print("---Zillow Synchronious Scraper with ScraperAPI---")
    print()

    test = True
    if test is False:
        proceed = input("Enter y to start Or anything else to quit: ")
        if proceed == 'y':
            state = input("Enter State. NY or NJ: ")
            price = input("Enter Starting Price: ")
            
            data = main(links[state], int(price))
        else: sys.exit("Exiting Program")
    else:
        data = main(links['NY'], int(4000001))

    
