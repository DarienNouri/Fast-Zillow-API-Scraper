#
from datetime import date, timedelta, datetime
import random
from ParseJSON import * 
from scraper_api import ScraperAPIClient
from pathlib import Path
import concurrent.futures
from concurrent import futures
import csv
import urllib
import logging

class Zillow:

    def __init__(self):
        self.start = time.time()
        self.API_KEY = '494f207eb22c2f7df82afa4943654c5e'
        self.listingDatabase = []
        self.starting_price = 0
        self.previous_price = 0
        self.current_price = 0
        self.local_max_price = 0
        self.current_url = ''
        self.input_url = ''
        self.start_url = ''
        self.end_url = ''
        self.soup = BeautifulSoup()
        self.save_name = ''
        self.page = 2
        self.url = ''
        self.random_num = str(random.randrange(13, 99))
        self.end = False
        

    def parseAllDataSections(self, soup=None):
        if soup: self.soup = soup
        listing_data = {}
        parsedJson = parseJSON(self.soup)
        nestedData = getNestedData(parsedJson)
        listing_data.update(generalData(parsedJson))
        listing_data.update(adressData(nestedData))
        listing_data.update(propertyFeaturesData(nestedData))
        listing_data.update(forclosureData(nestedData))
        listing_data.update(listingAgentData(nestedData))
        listing_data.update(nearbySchoolData(nestedData))
        listing_data.update(priceHistoryData(nestedData))
        
        if listing_data['price'] > self.local_max_price:
            self.local_max_price = listing_data['price']
        if self.local_max_price < self.previous_price - 1:
            self.end = True
            return False
        if self.end is not True:
            self.listingDatabase.append(listing_data)
        self.async_count = 0
        if len(listing_data) != 0:
            return listing_data
        else:
            return False
    

    def parseInputUrl(self, input_url_: str):
        self.input_url = input_url_
        url_find = self.input_url.find('price%')
        self.start_url = self.input_url[:(self.input_url.find('%22min%22%'))+12]
        last_segment = self.input_url[(self.input_url.find('%22min%22%'))+12:]
        self.end_url = last_segment[last_segment.find('%'):]
        self.input_url = self.start_url+str(self.current_price)+self.end_url
        self.url = self.start_url+str(self.current_price)+self.end_url##
        return self.input_url
    

    def updateUrlPrice(self, price: int, first_run=False):
        if first_run is False and self.previous_price == self.current_price:
            self.current_price+=1
        self.input_url = self.start_url+str(self.current_price)+self.end_url
        self.current_url = self.start_url+str(self.current_price)+self.end_url
        self.url = self.start_url+str(self.current_price)+self.end_url##
        self.previous_price = self.current_price
        return self.url


    def updateUrlPage(self, page_num_):
        page_num = page_num_
        url_find = self.current_url.find('currentPage')
        url_start = self.current_url[:url_find+17]
        if self.page <10:
            url_end = self.current_url[url_find+18:]
        elif 100 > self.page >= 10:
            url_end = self.input_url[url_find+18:]
        self.current_url = url_start+str(page_num)+url_end
        return self.current_url
    

    def getListingLinks(self):
        try:
            params = {'api_key': self.API_KEY, 'url': self.current_url}
            response = requests.get('http://api.scraperapi.com/', params=urllib.parse.urlencode(params))
            html_response = response.text
            soup = BeautifulSoup(html_response, "html.parser")
            data = json.loads(soup.select_one("script[data-zrr-shared-data-key]").contents[0].strip("!<>-")) 
            listing_links = []
            all_data = data['cat1']['searchResults']['listResults']
            for i in range(len(all_data)):
                link = all_data[i]['detailUrl']
                    # sometimes the link does not contain the starting website url, thats why we are inserting "https://www.zillow.com{link}" at the starting of link
                if 'http' not in link:
                        link_to_buy = f"https://www.zillow.com{link}"
                        listing_links.append(link_to_buy)
                else:
                        link_to_buy = link
                        listing_links.append(link_to_buy)
            return listing_links
        except:
            return None


    def sendRequest(self,url):
               
                apiKey = '494f207eb22c2f7df82afa4943654c5e'
                client = ScraperAPIClient(apiKey)
                #Requests Users
                try:
                    result = client.get(url = url, render=True)
                    self.soup = BeautifulSoup(result.content,features="lxml")
                    return self.soup
                except:
                    return None



    def async_scrape_url(self, url):  ## Function to process requests concurrently
        NUM_RETRIES = 3
        self.async_count+=1
        params = {'api_key': self.API_KEY, 'url': url}
        for _ in range(NUM_RETRIES):
            try:
                response = requests.get('http://api.scraperapi.com/', params=urllib.parse.urlencode(params))
                if response.status_code in [200, 404]:
                    break ## escape for loop if the API returns a successful response
            except requests.exceptions.ConnectionError:
                response = ''
        if response.status_code != 200: ## parse data if 200 status code (successful response)
            print('bad request')
        else:
            try:
                html_response = response.text
                soup = BeautifulSoup(html_response, "html.parser")  
                            
            except:
                return False
            return self.parseAllDataSections(soup)  

   



    def sub(self, executor, listing_links):
        try:
            futures = executor.map(self.async_scrape_url, listing_links, timeout=18)
          
        
        except concurrent.futures._base.TimeoutError:
            logging.info('map timed out!')  # this is never logged
            raise

        try:
            results = list(futures)
        except concurrent.futures._base.TimeoutError:
            logging.info('list timed out!')  # here it happens!
            raise

        logging.info(results)
        logging.info('sub done')
        return len(results)

    def download_many1(self, listing_links):  # without context manager
        logging.info('download_many1')
        executor = futures.ThreadPoolExecutor(20)
        return self.sub(executor, listing_links)
        
    def runAsync(self,listing_links):
        NUM_THREADS = 20
        outputs= []
        with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
                    results = executor.map(self.async_scrape_url, listing_links, timeout=14)
                    
                    try:
                        for i in results:
                            outputs.append(i)
                    except futures._base.TimeoutError:
                        print("TIMEOUT")
                    print(outputs)
    
    def runAsync(self,listing_links):
        NUM_THREADS = 20
        outputs= []
        with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
                future_to_url = {executor.submit(self.async_scrape_url, url): url for url in listing_links}
                for future in concurrent.futures.as_completed(future_to_url):
                    
                    
                    soup = future.result()
                    try:
                        self.parseAllDataSections(soup)
                       
                    except futures._base.TimeoutError:
                        print("TIMEOUT")

              
 
    def captchaCheck(self, soup=None):
        if soup: 
            self.soup = soup
        try:
            text = self.soup.find(class_="zsg-layout-content").find('div').find('div').text
            if text == "Please verify you're a human to continue.":
                print(text)
                raise Exception(text)
        except:
            return False


    def transformRawData(self, listingsDatabase_):
        df = pd.DataFrame(listingsDatabase_)
        return df

    

    def getSaveName(self): 
        file_name_num = 1
        path = '../OUTPUT/cleaned_excel/' 
        os.makedirs(path, exist_ok=True) 
        today = date.today()
        df = self.transformRawData(self.listingDatabase)
        while True:   
            save_name = df['state'][0]+'-'+str(today.month)+'-'+str(today.day)+'_'+str(file_name_num)                    
            file_path = path+save_name+'.xlsx'
            my_file = Path(file_path)
            if my_file.is_file():
                file_name_num+=1
            else:
                self.save_name = save_name 
                return self.save_name


    def saveCSV(self, df=None):
        count = 0
        try:
            if df is None: df = self.transformRawData(self.listingDatabase)
        except:
            while df is None:
                count+=1
                del self.listingDatabase[-1]
                df = self.transformRawData(self.listingDatabase)
                if count == 41: sys.exit("issue saving csv file. Tried removing listings from end in while loop "+str(count)+" many times")

                
            print(self.listingDatabase[-50:])
            print('num listings deleted from end: '+ str(count))
        path = '../OUTPUT/raw_csv/'
        os.makedirs(path, exist_ok=True)
        csv_path = path+self.save_name+'.csv'
        df.to_csv(csv_path)
   

    def create_excel(self, df = None):  
        #
        # ---Data-Preprocessing--- Remove Duplicate Emails and format datatypes
        #  
        df_og = self.transformRawData(self.listingDatabase)
        params = ['price', 'streetAddress', 'city', 'zipcode','state','daysOnZillow','agentName','agentEmail', 'agentPhoneNumber','hdpUrl']
        df_a = df_og[params]
        df = df_a.sort_values(['agentName','price'],
                    ascending = [False, False])
        try:           
            df = df[~df.agentName.str.contains('Team') ]
        except: pass
        og_len = len(df)
        df_drop = df.drop_duplicates('agentName',ignore_index=True)
        drop_len = len(df_drop)
        df_drop= df_drop.sort_values(['price'],
                    ascending = [False])
        df = df_drop
        df['First'] = df.agentName.apply(
        lambda x: pd.Series(str(x).split(" ")[0]))
        df['agentName']
        df['Last'] = df.agentName.apply(
        lambda x: pd.Series(str(x).split("-")[-1].split(' ')[-1]))
        cols = [ 'streetAddress', 'price', 'city', 'zipcode', 'state', 'First', 'Last',    'agentEmail', 'agentPhoneNumber', 'daysOnZillow', 'hdpUrl']
        df = df[cols]
        df.columns = [ 'Street', 'Price', 'City', 'Zipcode', 'State', 'First', 'Last',    'AgentEmail', 'AgentPhoneNumber', 'DaysOnZillow', 'hdpUrl']
        df['Price'] = df['Price'].astype(float).astype("Int32").apply(\
                                lambda x: "${:,.0f}".format(x) if isinstance(x, int) else x)
        df =df[df.AgentEmail.str.contains("@",na=False)]
        df =df.loc[df['DaysOnZillow'] < 365].reset_index(drop=True)
        #
        #---Write dataframe to Excel---
        #
        path = '../OUTPUT/cleaned_excel/' 
        os.makedirs(path, exist_ok=True)   
        writer = pd.ExcelWriter(path+self.save_name+'.xlsx', engine='xlsxwriter',mode='w')
        df.to_excel(writer, sheet_name= self.save_name, index = False)
        workbook  = writer.book
        worksheet = writer.sheets[self.save_name]                       
        header_format = workbook.add_format({'bold': True, 'text_wrap': True, 'fg_color': '#b38dd6'})
        cf = workbook.add_format()
        worksheet.set_column('A:A', 30,cf)
        worksheet.set_column('B:B', 14,cf)
        worksheet.set_column('A:A', 20,cf)
        worksheet.set_column('C:C', 20,cf)
        worksheet.set_column('D:D', 9,cf)
        worksheet.set_column('E:E', 6,cf)
        worksheet.set_column('F:G', 16,cf)
        worksheet.set_column('H:H', 28,cf)
        worksheet.set_column('J:J', 19,cf)
        worksheet.set_column('K:K', 13,cf)
        worksheet.set_column('I:I', 35,cf)
        worksheet.set_column('L:L', 100,cf)
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
        worksheet.set_row(1,1,cf)
        writer.save()  
                      
    def exitProgram(self):
        print('Previous Price:',self.listingDatabase[-4]['price'])
        print('Current Price:',self.current_price)
        print('Starting Price:', self.starting_price)
        print('Listing Count:',len(self.listingDatabase)) 
        self.saveCSV()
        self.create_excel()    
        end = time.time()
        temp = end-self.start
        hours = temp//3600
        temp = temp - 3600*hours
        minutes = temp//60
        seconds = temp - 60*minutes
        print('Elapsed time: ' + '%d:%d:%d' %(hours,minutes,seconds))



