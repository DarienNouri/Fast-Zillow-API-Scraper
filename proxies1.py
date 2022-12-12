from pyppeteer import launch
from bs4 import BeautifulSoup
import pandas as pd
import asyncio

async def get_html():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://www.zillow.com/nj/2_p/?searchQueryState=%7B%22pagination%22%3A%7B%22currentPage%22%3A2%7D%2C%22usersSearchTerm%22%3A%22NJ%22%2C%22mapBounds%22%3A%7B%22west%22%3A-76.7952458515625%2C%22east%22%3A-72.6534001484375%2C%22south%22%3A38.68416008936318%2C%22north%22%3A41.45789958695567%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A40%2C%22regionType%22%3A2%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22mp%22%3A%7B%22min%22%3A1436%7D%2C%22sort%22%3A%7B%22value%22%3A%22pricea%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22price%22%3A%7B%22min%22%3A300000%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A8%7D')
    await page.waitForSelector("div.board-member", visible=True)
    html = await page.content()
    await browser.close()
    return html

html = asyncio.get_event_loop().run_until_complete(get_html())
soup = BeautifulSoup(html, "html.parser")