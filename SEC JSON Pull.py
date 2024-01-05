# -*- coding: utf-8 -*-
"""

SEC Filing Scraper
@author: Calebfinance

"""

# import modules
import requests
import pandas as pd
import matplotlib.pyplot as plt

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
companyFacts.json()['facts']['us-gaap']['EarningsPerShareDiluted']

# get company concept data - example is EPS as noted above
companyConcept = requests.get(
    (
    f'https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}'
     f'/us-gaap/EarningsPerShareDiluted.json'
    ),
    headers=headers
    )

# review data
companyConcept.json().keys()
companyConcept.json()['units']
companyConcept.json()['units'].keys()
companyConcept.json()['units']['USD/shares']
companyConcept.json()['units']['USD/shares'][0]

# parse assets from single filing
companyConcept.json()['units']['USD/shares'][0]['val']

# get all assets data for all time periods
assetsData = pd.DataFrame.from_dict((
               companyConcept.json()['units']['USD/shares']))

# review data
assetsData.columns
assetsData.form

# get assets from 10K forms and reset index
assets10K = assetsData[assetsData.form == '10-K']
assets10K = assets10K.reset_index(drop=True)

#created CSV to review the output
csv_file_path = "assets10K.csv"
# Save the DataFrame to a CSV file
assets10K.to_csv(csv_file_path, index=False)  # Set index=False to exclude the index column
print(f"CSV file will be saved at: {csv_file_path}")

# Generate a list of desired year values from 'CY2009' to 'CY2023'
desired_years = [f'CY{i}' for i in range(2009, 2024)]

# Filter the DataFrame based on the "frame" column
assets10K_filtered = assets10K[assets10K['frame'].isin(desired_years)]

# Reset the index and drop the old index column
assets10K_filtered = assets10K_filtered.reset_index(drop=True)

# Now, assets10K_filtered contains only the rows with the desired "frame" values from CY2009 to CY2023.

# plot 
assets10K_filtered.plot(x='end', y='val')

assets10K_filtered.sort_values(by='end', ascending=True, inplace=True)

# Slice the DataFrame to select the last 12 years
assets_last_12_years = assets10K_filtered.tail(12)

# Assuming your DataFrame is named assets_last_12_years
plt.figure(figsize=(12, 6))

# Create a bar chart with "end" as x-axis and "val" as the height of the bars
plt.bar(assets_last_12_years['end'], assets_last_12_years['val'], color='skyblue', alpha=0.7)

# Add data labels on top of each bar
for i, val in enumerate(assets_last_12_years['val']):
    plt.text(assets_last_12_years['end'].iloc[i], val, str(val), ha='center', va='bottom')

plt.xticks(rotation=45)
plt.xlabel('Fiscal Year')
plt.ylabel('EPS')
plt.title('Last 12 Years of Data')
plt.grid(True)
plt.show()
