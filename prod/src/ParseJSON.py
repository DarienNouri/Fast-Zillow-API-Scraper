import sys
import requests
import json
import html
import time
import nest_asyncio
import traceback
import pandas as pd
nest_asyncio.apply()
from datetime import datetime
from bs4 import BeautifulSoup
import os
#sys.path.insert(1, r'C:\Users\darie\OneDrive - nyu.edu\PyCharm Projects\mishaScraperPrj\olderVersions\src')
import importlib
#import allFunctions as zillow
#importlib.reload(zillow)
from datetime import datetime
utcCurrentTime = str(datetime.utcnow())



def parseJSON(soup):
    
    data = json.loads(soup.find("script", {"id": "hdpApolloPreloadedData"}).contents[0].strip("!<>-\\"))
                #store JSON Data in Variable final
    rawPayload = json.loads(data['apiCache'])
    payloadDict = rawPayload[list(rawPayload.keys())[1]]
    return rawPayload
#
def generalData(parsedJson:dict):
        unNestedKeys = [ 'zpid', 'homeStatus', 'bedrooms', 'bathrooms', 'price', 'yearBuilt', 'isRentalListingOffMarket', 'contingentListingType',
        'pageViewCount', 'daysOnZillow', 'longitude', 'latitude','hdpUrl', 'desktopWebHdpImageLink', 'timeZone', 'brokerId', 'monthlyHoaFee', 'propertyTaxRate', 'lotSize']
        firstNestPairs = {}
        for key in unNestedKeys:
            try:
                firstNestPairs[key] = parsedJson[list(parsedJson.keys())[1]]['property'][key]
            except:
                firstNestPairs[key] = 'nan'
        firstNestPairs['hdpUrl'] = 'zillow.com/' + firstNestPairs['hdpUrl']
        # self.master_Dict.update(firstNestPairs)
        firstNestPairs['utcScrapeTime'] = utcCurrentTime
        return firstNestPairs


def getNestedData(parsedJson:dict):
    nestedValues = ['address', 'listing_sub_type', 'resoFacts', 'attributionInfo', 'schools', 'taxHistory', 'priceHistory', 'mortgageRates', 'resoFacts']
    nestedData = {}
    for key in nestedValues: 
        nestedData[key] = parsedJson[list(parsedJson.keys())[1]]['property'][key]
    # self.master_Dict.update(nestedData)
    return nestedData


def adressData(nestedData:dict):
        addressKeys = ['streetAddress', 'city', 'state', 'zipcode']
        addressData = {}
        for i in nestedData['address']:
            if i in addressKeys:
                addressData[i] = nestedData['address'][i]
        #self.master_Dict.update(addressData)
        return addressData


def forclosureData(nestedData:dict):
    #self.master_Dict.update(nestedData['listing_sub_type'])
    return nestedData['listing_sub_type']



def propertyFeaturesData(nestedData:dict):
    propertyFeaturesKeys = ['hasAssociation','associationFee','buildingName','buyerAgencyCompensation','buyerAgencyCompensationType','hasAssociation','basement','canRaiseHorses','coveredParkingCapacity','fireplaces','hasGarage','hasFireplace','parkingCapacity','pricePerSquareFoot','stories','hasRentControl','structureType','hasPrivatePool','hasWaterfrontView']
    propertyFeaturesData = {}
    for i in nestedData['resoFacts']:
        if i in propertyFeaturesKeys:
            propertyFeaturesData[i] = nestedData['resoFacts'][i]
    #self.master_Dict.update(propertyFeaturesData)
    return propertyFeaturesData


def listingAgentData(nestedData:dict):
    listingAgentKeys = ['listingAgreement','agentEmail','agentName','agentPhoneNumber','brokerName','brokerPhoneNumber']
    listingAgentData = {}
    for i in nestedData['attributionInfo']:
        if i in listingAgentKeys:
            listingAgentData[i] = nestedData['attributionInfo'][i]
    try:
        listingAgentData['First'] = listingAgentData['agentName'].split(" ")[0]
        listingAgentData['Last'] = listingAgentData['agentName'].split("-")[-2].split(' ')[1]
    except:
        listingAgentData['First'] = ''
        listingAgentData['Last'] = ''
    
    

    #self.master_Dict.update(listingAgentData)
    return listingAgentData


def nearbySchoolData(nestedData:dict):
    schoolKeys = [ 'rating']
    schoolDesiredValues = []
    for i in nestedData['schools']:
        for x in i:
            if x in schoolKeys:
                schoolDesiredValues.append( i[x])
    try:
        avgSchoolRating = {'averageSchoolRating': round(sum(schoolDesiredValues)/len(schoolDesiredValues), 2)}
    except:
        avgSchoolRating = {'averageSchoolRating': 'NaN'}
    
    return avgSchoolRating
    
def priceHistoryData(nestedData:dict):
    priceHistData = {}
    histData = []
    price_hist = {'priceHistory':['event','price','date','priceChangeRate','event','sellerAgent','source']}
    for i in nestedData['priceHistory']:
        price_temp = {}
        for key, value in price_hist.items():
            for item in value:           
                price_temp[item] = [i][0][item]     
            priceHistData[[i][0]['date']] = price_temp
            histData.append({[i][0]['date']:price_temp})
    
    return {'priceHistory':histData}



        
