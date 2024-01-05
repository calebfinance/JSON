# SEC Filing Scraper

This Python script is designed to scrape and process SEC filings. It fetches data from the SEC's website and formats it for further analysis.

## Requirements

To run this script, you'll need the following Python modules:
- `requests`: For making HTTP requests to the SEC website.
- `pandas`: For data manipulation and analysis.

## Installation

To install the required modules, run:
pip install requests pandas


## Usage

To use the script, simply run it in your Python environment. The script will automatically fetch and process the latest SEC filings data.

Example command:
python SEC_JSON_Pull.py


## Output

The script outputs a dictionary containing SEC filings data. Here's an example of what the output might look like:

```python
{
  'ticker': 'AAPL',
  'company_name': 'Apple Inc.',
  'form_type': '10-K',
  'date_filed': '2022-10-30',
  'file_url': 'https://www.sec.gov/Archives/edgar/data/320193/000032019320000096/a10-k20200926.htm'
}
Note: The above output is a hypothetical example and may differ from the actual output of the script.
