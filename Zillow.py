
from datetime import date, timedelta, datetime
import random
from ParseJSON import * 
from scraper_api import ScraperAPIClient
class Zillow:

    def __init__(self):
      
        self.listingDatabase = []
        self.previous_price = 0
        self.current_price = 0
        self.current_url = ''
        self.input_url = ''
        self.start_url = ''
        self.end_url = ''
        self.soup = BeautifulSoup()
        
        self.page = 2
        self.url = ''
        self.random_num = str(random.randrange(13, 99))
        self.req_headers = ''
        self.header_bank = [{
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.8',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951 Safari/537.36'
        },
        {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': 'zguid=23|%24ca6368b9-7b92-4d51-ab67-c2be89065efd; _ga=GA1.2.1460486079.1621047110; _pxvid=7fa13d96-b528-11eb-9860-0242ac120012; _gcl_au=1.1.2025797213.1621047113; __gads=ID=66253ab863481044:T=1621047113:S=ALNI_MZr3mehwm2Wjo7NOrmalVtEcJSXag; __pdst=50987f626deb4767a53b5d8ca2ea406a; _fbp=fb.1.1621047115574.1019382068; _pin_unauth=dWlkPU5EVm1PRGRpTVRBdE5UTTFaUzAwWlRBNExUZzJZall0TWpZMU1HWTBNV0ppWlRkbA; G_ENABLED_IDPS=google; userid=X|3|231a9d744e104379%7C3%7CiEt8bkUx9hWaFeyCeAwN9tHl_T0d0Cq-kynGuEvNYr4%3D; loginmemento=1|c2274ba4a4ad76bbe89263d30695c182e9177b9c40a2691f3054987d66a944be; zjs_user_id=%22X1-ZU158jhpb2klds9_4wzn7%22; zgcus_lbut=; zgcus_aeut=189997416; zgcus_ludi=b44a961b-c7ef-11eb-a48f-96824e7eff50-18999; optimizelyEndUserId=oeu1623111792776r0.8778663892923859; _cs_c=1; WRUIDAWS=3326630244368428; visitor_id701843=248614376; visitor_id701843-hash=4be116fbd77089f953bfb6eaf5996ef92662a6ef7d237d3c49f154ffaf4eaa9295c64fb254b106bdff234e183c94498c01af2aab; __stripe_mid=80125db1-17d1-4fc5-ae37-86b12a68709cf3da6d; g_state={"i_p":1627697570928,"i_l":4}; zjs_anonymous_id=%22ca6368b9-7b92-4d51-ab67-c2be89065efd%22; _gac_UA-21174015-56=1.1626042638.Cj0KCQjwraqHBhDsARIsAKuGZeH8gi095UkXfohW-WWvyLosdmTdL8cfJwgAabYF9hS2XU6JlXqpWLcaAq5SEALw_wcB; _gcl_aw=GCL.1626042640.Cj0KCQjwraqHBhDsARIsAKuGZeH8gi095UkXfohW-WWvyLosdmTdL8cfJwgAabYF9hS2XU6JlXqpWLcaAq5SEALw_wcB; zgsession=1|1edd82e6-372a-4546-bc8b-c2bbadfd29b4; DoubleClickSession=true; fbc=fb.1.1626412984774.IwAR2QM6bzrTskAWN5Sk8UnmPlAxb1HRy1h1GRch888QqXfczHZZWb2vDZfIw; _fbc=fb.1.1626413249162.IwAR2QM6bzrTskAWN5Sk8UnmPlAxb1HRy1h1GRch888QqXfczHZZWb2vDZfIw; _csrf=lV2BBFim7Vy2gFTn--PUt0VA; _gaexp=GAX1.2.w27igyYtRQaAa8XQM3MjDw.18837.2!VDVoDKTnRcyv8f4FAcJ8PA.18915.2!Khnq27RoQmSe5DEusmh5xA.18913.3; _gid=GA1.2.705011419.1630004829; FSsampler=707279376; __CT_Data=gpv=26&ckp=tld&dm=zillow.com&apv_82_www33=26&cpv_82_www33=26&rpv_82_www33=13; OptanonConsent=isIABGlobal=false&datestamp=Fri+Aug+27+2021+12%3A39%3A52+GMT-0600+(Mountain+Daylight+Time)&version=5.11.0&landingPath=NotLandingPage&groups=1%3A1%2C3%3A1%2C4%3A1&AwaitingReconsent=false; _cs_id=41cbdc9c-bb0b-aad9-9521-b1328a65ff77.1623111795.22.1630089665.1630089591.1.1657275795752; utag_main=v_id:01796deff9e3001a59964343177e03079002907100838$_sn:41$_se:2$_ss:0$_st:1630255637884$dc_visit:38$ses_id:1630253822479%3Bexp-session$_pn:1%3Bexp-session$dcsyncran:1%3Bexp-session$tdsyncran:1%3Bexp-session$dc_event:2%3Bexp-session$dc_region:us-east-1%3Bexp-session$ttd_uuid:7b8796ca-44dd-45c9-97d9-bcb642d04cd1%3Bexp-session; JSESSIONID=6CB8C410E0FE216644E8C3A0D0851618; ZILLOW_SID=1|AAAAAVVbFRIBVVsVEklf443J474nftKzJe5PKLD80sujgHvySB7tGcqZunX3BDDH9VwceMqGMTPC54%2F0q4CH%2BfmwsC6P; KruxPixel=true; _derived_epik=dj0yJnU9ai1PSUp1eHZ2Y3J3d0c2NVU1N3BBOFlHbnRBOGFzT0smbj1vLWRISDFwdUNoblN5MjQ4cTVyN213Jm09MSZ0PUFBQUFBR0VzRjRVJnJtPTEmcnQ9QUFBQUFHRXNGNFU; KruxAddition=true; search=6|1632872450375%7Crect%3D40.241821806991595%252C-103.77545313688668%252C39.18758562803622%252C-106.02765040251168%26disp%3Dmap%26mdm%3Dauto%26type%3Dhouse%252Cmultifamily%252Ctownhouse%26fs%3D1%26fr%3D0%26mmm%3D1%26rs%3D0%26ah%3D0%09%0911093%09%09%09%09%09%09; _uetsid=d5e0465006a011ecbe3bd1a0f1c47d01; _uetvid=987e1c70c40a11ebaed8859af36f82fb; _px3=ba45c3df5d5d63d4d9780a102253cd60b21ab52b04778344e332e05474011c21:oCvapPXE6jD0rCXhSf4UjtEC2U956148EDyiWwRFOF8z5vwK63/hC8OWsk09O61g1spnZw64iXApZu1wOmKpyA==:1000:68UzJ5+ar5XwNm61bm41bhSHp8Zp1PfQQlL/5tcqdUIJ3RmA106//vvYGewCCwmln6acqbDAVKgqfB8Th05yX0Cw0TBW7dhfNdeNRjp9bxeLvKqZ56yuW+aVoYYp/zj6MNKv9c16vKlP771xSdCgUTvZ0CDmh7Ng55sHugOHt/jj+2Zmp2WLnuYR4rf7SEndqWBbAyQhhG4BKeyrZyEMpA==; AWSALB=3BIj2fUDeYgoAcLKaZdMkcyTzWSof62v91DQuCssJMyknlpZWcRcVnUU5Me29AcnFcjg1k9H2ehS6N0rSwxo4w8lmEvFCy6hgQfKm1HH8oVoWtpICS36NoLMMxmZ; AWSALBCORS=3BIj2fUDeYgoAcLKaZdMkcyTzWSof62v91DQuCssJMyknlpZWcRcVnUU5Me29AcnFcjg1k9H2ehS6N0rSwxo4w8lmEvFCy6hgQfKm1HH8oVoWtpICS36NoLMMxmZ',
            'referer': 'https://www.google.com/',
            'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
            'sec-ch-ua-mobile': '?1',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36'
        },
        {
    'authority': 'app.mybodygallery.com',
    'method': 'GET',
    'path': '/classes/Photo?where=%7B%22gender%22:%22female%22,%22status%22:%22APPROVED%22,%22weight%22:%7B%22$gte%22:47,%22$lte%22:53%7D%7D',
    'scheme': 'https',
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'referer': 'URL',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?1',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36'
},
{
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': 'zguid=23|%24ca6368b9-7b92-4d51-ab67-c2be89065efd; _ga=GA1.2.1460486079.1621047110; _pxvid=7fa13d96-b528-11eb-9860-0242ac120012; _gcl_au=1.1.2025797213.1621047113; __gads=ID=66253ab863481044:T=1621047113:S=ALNI_MZr3mehwm2Wjo7NOrmalVtEcJSXag; __pdst=50987f626deb4767a53b5d8ca2ea406a; _fbp=fb.1.1621047115574.1019382068; _pin_unauth=dWlkPU5EVm1PRGRpTVRBdE5UTTFaUzAwWlRBNExUZzJZall0TWpZMU1HWTBNV0ppWlRkbA; G_ENABLED_IDPS=google; userid=X|3|231a9d744e104379%7C3%7CiEt8bkUx9hWaFeyCeAwN9tHl_T0d0Cq-kynGuEvNYr4%3D; loginmemento=1|c2274ba4a4ad76bbe89263d30695c182e9177b9c40a2691f3054987d66a944be; zjs_user_id=%22X1-ZU158jhpb2klds9_4wzn7%22; zgcus_lbut=; zgcus_aeut=189997416; zgcus_ludi=b44a961b-c7ef-11eb-a48f-96824e7eff50-18999; optimizelyEndUserId=oeu1623111792776r0.8778663892923859; _cs_c=1; WRUIDAWS=3326630244368428; visitor_id701843=248614376; visitor_id701843-hash=4be116fbd77089f953bfb6eaf5996ef92662a6ef7d237d3c49f154ffaf4eaa9295c64fb254b106bdff234e183c94498c01af2aab; __stripe_mid=80125db1-17d1-4fc5-ae37-86b12a68709cf3da6d; g_state={"i_p":1627697570928,"i_l":4}; zjs_anonymous_id=%22ca6368b9-7b92-4d51-ab67-c2be89065efd%22; _gac_UA-21174015-56=1.1626042638.Cj0KCQjwraqHBhDsARIsAKuGZeH8gi095UkXfohW-WWvyLosdmTdL8cfJwgAabYF9hS2XU6JlXqpWLcaAq5SEALw_wcB; _gcl_aw=GCL.1626042640.Cj0KCQjwraqHBhDsARIsAKuGZeH8gi095UkXfohW-WWvyLosdmTdL8cfJwgAabYF9hS2XU6JlXqpWLcaAq5SEALw_wcB; zgsession=1|1edd82e6-372a-4546-bc8b-c2bbadfd29b4; DoubleClickSession=true; fbc=fb.1.1626412984774.IwAR2QM6bzrTskAWN5Sk8UnmPlAxb1HRy1h1GRch888QqXfczHZZWb2vDZfIw; _fbc=fb.1.1626413249162.IwAR2QM6bzrTskAWN5Sk8UnmPlAxb1HRy1h1GRch888QqXfczHZZWb2vDZfIw; _csrf=lV2BBFim7Vy2gFTn--PUt0VA; _gaexp=GAX1.2.w27igyYtRQaAa8XQM3MjDw.18837.2!VDVoDKTnRcyv8f4FAcJ8PA.18915.2!Khnq27RoQmSe5DEusmh5xA.18913.3; _gid=GA1.2.705011419.1630004829; FSsampler=707279376; __CT_Data=gpv=26&ckp=tld&dm=zillow.com&apv_82_www33=26&cpv_82_www33=26&rpv_82_www33=13; OptanonConsent=isIABGlobal=false&datestamp=Fri+Aug+27+2021+12%3A39%3A52+GMT-0600+(Mountain+Daylight+Time)&version=5.11.0&landingPath=NotLandingPage&groups=1%3A1%2C3%3A1%2C4%3A1&AwaitingReconsent=false; _cs_id=41cbdc9c-bb0b-aad9-9521-b1328a65ff77.1623111795.22.1630089665.1630089591.1.1657275795752; utag_main=v_id:01796deff9e3001a59964343177e03079002907100838$_sn:41$_se:2$_ss:0$_st:1630255637884$dc_visit:38$ses_id:1630253822479%3Bexp-session$_pn:1%3Bexp-session$dcsyncran:1%3Bexp-session$tdsyncran:1%3Bexp-session$dc_event:2%3Bexp-session$dc_region:us-east-1%3Bexp-session$ttd_uuid:7b8796ca-44dd-45c9-97d9-bcb642d04cd1%3Bexp-session; JSESSIONID=6CB8C410E0FE216644E8C3A0D0851618; ZILLOW_SID=1|AAAAAVVbFRIBVVsVEklf443J474nftKzJe5PKLD80sujgHvySB7tGcqZunX3BDDH9VwceMqGMTPC54%2F0q4CH%2BfmwsC6P; KruxPixel=true; _derived_epik=dj0yJnU9ai1PSUp1eHZ2Y3J3d0c2NVU1N3BBOFlHbnRBOGFzT0smbj1vLWRISDFwdUNoblN5MjQ4cTVyN213Jm09MSZ0PUFBQUFBR0VzRjRVJnJtPTEmcnQ9QUFBQUFHRXNGNFU; KruxAddition=true; search=6|1632872450375%7Crect%3D40.241821806991595%252C-103.77545313688668%252C39.18758562803622%252C-106.02765040251168%26disp%3Dmap%26mdm%3Dauto%26type%3Dhouse%252Cmultifamily%252Ctownhouse%26fs%3D1%26fr%3D0%26mmm%3D1%26rs%3D0%26ah%3D0%09%0911093%09%09%09%09%09%09; _uetsid=d5e0465006a011ecbe3bd1a0f1c47d01; _uetvid=987e1c70c40a11ebaed8859af36f82fb; _px3=ba45c3df5d5d63d4d9780a102253cd60b21ab52b04778344e332e05474011c21:oCvapPXE6jD0rCXhSf4UjtEC2U956148EDyiWwRFOF8z5vwK63/hC8OWsk09O61g1spnZw64iXApZu1wOmKpyA==:1000:68UzJ5+ar5XwNm61bm41bhSHp8Zp1PfQQlL/5tcqdUIJ3RmA106//vvYGewCCwmln6acqbDAVKgqfB8Th05yX0Cw0TBW7dhfNdeNRjp9bxeLvKqZ56yuW+aVoYYp/zj6MNKv9c16vKlP771xSdCgUTvZ0CDmh7Ng55sHugOHt/jj+2Zmp2WLnuYR4rf7SEndqWBbAyQhhG4BKeyrZyEMpA==; AWSALB=3BIj2fUDeYgoAcLKaZdMkcyTzWSof62v91DQuCssJMyknlpZWcRcVnUU5Me29AcnFcjg1k9H2ehS6N0rSwxo4w8lmEvFCy6hgQfKm1HH8oVoWtpICS36NoLMMxmZ; AWSALBCORS=3BIj2fUDeYgoAcLKaZdMkcyTzWSof62v91DQuCssJMyknlpZWcRcVnUU5Me29AcnFcjg1k9H2ehS6N0rSwxo4w8lmEvFCy6hgQfKm1HH8oVoWtpICS36NoLMMxmZ',
            'referer': 'https://www.google.com/',
            'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
            'sec-ch-ua-mobile': '?1',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36'
        }]




    
    def parseAllDataSections(self, soup=None):
        if soup:     self.soup = soup
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
        self.listingDatabase.append(listing_data)
        self.current_price = listing_data['price']
        
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
        self.soup = self.sendRequest(self.current_url)
        try:
            data = json.loads(self.soup.select_one("script[data-zrr-shared-data-key]").contents[0].strip("!<>-"))
        except:
            try:
                self.soup = self.sendRequest(self.current_url)
                data = json.loads(self.soup.select_one("script[data-zrr-shared-data-key]").contents[0].strip("!<>-"))
            except:
                return None
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

    def quickSave(self, df=None):
        if df is None: df = self.transformRawData(self.listingDatabase)
        path = 'output_dataBckup/raw_csv/'
        os.makedirs(path, exist_ok=True)
        today = date.today()
        
        save_name = path+df['state'][0]+'_'+str(today.month)+'_'+str(today.day)+'_'+self.random_num+'.csv'
        df.to_csv(save_name)
    
   
    def create_excel(self, dataframe):
        path = 'output_dataBckup/cleaned_excel/' 
        os.makedirs(path, exist_ok=True)      
        df_og =  dataframe
        params = ['price', 'streetAddress', 'city', 'zipcode','state','daysOnZillow','agentName','agentEmail', 'agentPhoneNumber','hdpUrl']
        df_a = df_og[params]
        df = df_a.sort_values(['agentName','price'],
                    ascending = [False, False])
        try:           
            df = df[~df.agentName.str.contains('Team') ]
        except:
            all = 'good'
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
        
        cols = [ 'streetAddress', 'price', 'city', 'zipcode', 'state', 'First', 'Last',    'agentEmail', 'agentPhoneNumber', 'daysOnZillow', 'hdpUrl'
        ]
        df = df[cols]
        df.columns = [ 'Street', 'Price', 'City', 'Zipcode', 'State', 'First', 'Last',    'AgentEmail', 'AgentPhoneNumber', 'DaysOnZillow', 'hdpUrl'
        ]
        df['Price'] = df['Price'].astype(float).astype("Int32").apply(\
                                lambda x: "${:,.0f}".format(x) if isinstance(x, int) else x)
        df =df[df.AgentEmail.str.contains("@",na=False)]
        df =df.loc[df['DaysOnZillow'] < 365].reset_index(drop=True)
        today = date.today()
     
        sheet = df['State'][0]+'_'+str(today.month)+'_'+str(today.day)+'_'+self.random_num                    
        file_name = sheet +'_cleaned.xlsx'
        # file_name = df_og.iloc[3]['scrapeID']+'_cleaned.xlsx'
        print(path+sheet+'.xlsx')
        writer = pd.ExcelWriter(path+sheet+'.xlsx', engine='xlsxwriter',mode='w')
        df.to_excel(writer, sheet_name= sheet, index = False)
        workbook  = writer.book
        worksheet = writer.sheets[sheet]                       
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
        
                      
    



            


        

