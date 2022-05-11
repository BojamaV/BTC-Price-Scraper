from bs4 import BeautifulSoup
import requests
import re
from datetime import timezone
import datetime
import json
import os
import schedule
import time

url = 'https://coinmarketcap.com/currencies/bitcoin/'

def run_scraper():
  print('running')
  data = []

  if os.path.exists('dogecoin_prices.json'):
    with open('dogecoin_prices.json') as f:
      data = json.load(f)

  content = requests.get(url).text
  soup = BeautifulSoup(content, 'lxml')


  
  regex = re.compile('.*priceValue.*')

  
  current_price = soup.find('div', {'class': regex}).text
  print(current_price)

  
  dt = datetime.datetime.now(timezone.utc)

  utc_time = dt.replace(tzinfo=timezone.utc)
  utc_timestamp = utc_time.timestamp()

  
  export_object = {
    'time': utc_timestamp,
    'price': current_price
  }
  print(export_object)

  data.append(export_object)

  with open('bitcoin_prices.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

schedule.every(6).seconds.do(run_scraper)

while True:
  schedule.run_pending()
  time.sleep(1)
