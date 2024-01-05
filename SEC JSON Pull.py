# -*- coding: utf-8 -*-
"""

SEC Filing Scraper
@author: AdamGetbags

"""

# import modules
import requests
import pandas as pd

# create request header
headers = {'User-Agent': "caleb@409a.fyi"}

# get all companies data / stored as a dictionary
companyTickers = requests.get(
    "https://www.sec.gov/files/company_tickers.json",
    headers=headers
    )

# review response / keys
print(companyTickers.json().keys())

# format response to dictionary and get first key/value
firstEntry = companyTickers.json()['0']

# parse CIK // without leading zeros
directCik = companyTickers.json()['0']['cik_str']

# dictionary to dataframe
companyData = pd.DataFrame.from_dict(companyTickers.json(),
                                     orient='index')

# add leading zeros to CIK
companyData['cik_str'] = companyData['cik_str'].astype(
                           str).str.zfill(10)

# review data
print(companyData[:1])

#Add leading 0s to match Edgar keys for the company
cik = companyData[0:1].cik_str[0]

# get company specific filing metadata
filingMetadata = requests.get(
    f'https://data.sec.gov/submissions/CIK{cik}.json',
    headers=headers
    )

# review json 
print(filingMetadata.json().keys())
filingMetadata.json()['filings']
filingMetadata.json()['filings'].keys()
filingMetadata.json()['filings']['recent']
#what are the fields of data to classify filings
filingMetadata.json()['filings']['recent'].keys()

# dictionary to dataframe
allForms = pd.DataFrame.from_dict(
             filingMetadata.json()['filings']['recent']
             )

# review columns
allForms.columns
#Just check on the data for the first 50 results with the columns 'accessionNumber', 'reportDate', 'form'
allForms[['accessionNumber', 'reportDate', 'form']].head(50)

# 10-K metadata is on line 3
allForms.iloc[3]

# get company facts data to parse through to get to company concepts
companyFacts = requests.get(
    f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json',
    headers=headers
    )

#review data
companyFacts.json().keys()
companyFacts.json()['facts']
#what are the types of data in "facts" - DEI and US GAAP
companyFacts.json()['facts'].keys()

# filing metadata for "EntityCommonStockSharesOutstanding" based on "dei"
companyFacts.json()['facts']['dei'][
    'EntityCommonStockSharesOutstanding']
# for chosen metadata, what are the columns - 'label', 'description', 'units'
companyFacts.json()['facts']['dei'][
    'EntityCommonStockSharesOutstanding'].keys()
# pulling the units to get the values
companyFacts.json()['facts']['dei'][
    'EntityCommonStockSharesOutstanding']['units']
# for chosen metadata, what are the keys -- shares
companyFacts.json()['facts']['dei'][
    'EntityCommonStockSharesOutstanding']['units'].keys()
#now have a list of metadata that can be sorted
companyFacts.json()['facts']['dei'][
    'EntityCommonStockSharesOutstanding']['units']['shares']
companyFacts.json()['facts']['dei'][
    'EntityCommonStockSharesOutstanding']['units']['shares'][0]


# concept data // financial statement line items
companyFacts.json()['facts']['us-gaap']
companyFacts.json()['facts']['us-gaap'].keys()

# different amounts of data available per concept
companyFacts.json()['facts']['us-gaap']['AccountsPayable']
companyFacts.json()['facts']['us-gaap']['Revenues']
companyFacts.json()['facts']['us-gaap']['Assets']

# get company concept data - example is Assets as noted above
companyConcept = requests.get(
    (
    f'https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}'
     f'/us-gaap/Assets.json'
    ),
    headers=headers
    )

# review data
companyConcept.json().keys()
companyConcept.json()['units']
companyConcept.json()['units'].keys()
companyConcept.json()['units']['USD']
companyConcept.json()['units']['USD'][0]

# parse assets from single filing
companyConcept.json()['units']['USD'][0]['val']

# get all assets data for all time periods
assetsData = pd.DataFrame.from_dict((
               companyConcept.json()['units']['USD']))

# review data
assetsData.columns
assetsData.form

# get assets from 10Q forms and reset index
assets10Q = assetsData[assetsData.form == '10-Q']
assets10Q = assets10Q.reset_index(drop=True)

# plot 
assets10Q.plot(x='end', y='val')
