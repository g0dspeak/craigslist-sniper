from craigslist import CraigslistForSale
from twilio.rest import TwilioRestClient
from pyshorteners import Shortener
from pprint import pformat
from config import *
import time


known_listings = {}
query = CraigslistForSale(site=CL_SITE,
                          filters={'search_titles': True,
                                   'query': CL_QUERY,
                                   'min_price': MIN_PRICE,
                                   'max_price': MAX_PRICE})

sms_client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
url_shortener = Shortener('Tinyurl')

while True:
    results = query.get_results(limit=10, sort_by="newest")
    for result in results:

        if result['id'] not in known_listings and CL_SITE in result['url']:
            known_listings[result['id']] = result

            with open('log.txt', 'a') as _f:
                _f.write('\n' + pformat(result))

            short_url = url_shortener.short(result['url']).split('://')[1]
            message_body = "New Listing:\n\n{0}\n\n{1}\n\n{2}".format(result['name'],
                                                                      result['price'],
                                                                      short_url)
            sms_client.messages.create(to=TO_NUMBER, from_=FROM_NUMBER,
                                       body=message_body)
            time.sleep(5)

    time.sleep(20)
