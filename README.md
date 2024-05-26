# Zillow Listing Web Scraper

This repository contains a Zillow Listing Web Scraper, designed for academic purposes and used for research at New York University. The scraper extracts detailed property information from Zillow, including general data, address data, property features, foreclosure data, listing agent information, nearby schools, and price history.

## Features

- Extracts detailed property information from Zillow
- Utilizes concurrent processing for efficient scraping
- Saves the collected data in CSV and Excel formats

## Usage

1. Update the `API_KEY` in the `Zillow` class with your ScraperAPI key.

2. To start scraping, initialize the `Zillow` class and call the appropriate methods:
    ```python
    from zillow_scraper import Zillow

    scraper = Zillow()
    input_url = "your_initial_zillow_url"
    scraper.parseInputUrl(input_url)
    listing_links = scraper.getListingLinks()
    scraper.runAsync(listing_links)
    scraper.exitProgram()
    ```

## Methods

- `parseAllDataSections(soup)`: Parses all data sections from the provided BeautifulSoup object.
- `parseInputUrl(input_url)`: Parses the input URL to prepare it for scraping.
- `updateUrlPrice(price, first_run)`: Updates the URL with the new price for scraping.
- `updateUrlPage(page_num)`: Updates the URL with the new page number for scraping.
- `getListingLinks()`: Retrieves the listing links from the current URL.
- `sendRequest(url)`: Sends a request to the provided URL using ScraperAPI.
- `async_scrape_url(url)`: Asynchronously scrapes the URL.
- `sub(executor, listing_links)`: Sub-method for concurrent scraping.
- `download_many1(listing_links)`: Initiates concurrent scraping without context manager.
- `runAsync(listing_links)`: Runs asynchronous scraping.
- `captchaCheck(soup)`: Checks for CAPTCHA in the provided BeautifulSoup object.
- `transformRawData(listingsDatabase)`: Transforms the raw data into a DataFrame.
- `getSaveName()`: Generates a save name for the output file.
- `saveCSV(df)`: Saves the DataFrame to a CSV file.
- `create_excel(df)`: Creates an Excel file from the DataFrame.
- `exitProgram()`: Exits the program and saves the scraped data.

## License

This project is intended solely for educational and research purposes. Please do not use it for any commercial purposes or in violation of Zillow's terms of service.

## Acknowledgments

This project was used for research at New York University.

---

**Disclaimer**: This scraper is intended for academic purposes only. The use of this code is at your own risk.
