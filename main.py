import requests
import os
# import lxml
from bs4 import BeautifulSoup
import smtplib

URL = ("https://www.amazon.ca/EZBASICS-Extendable-Humidifier-Moisturizing-Atomizer/dp/B086KSXF4H/"
       "ref=sr_1_5?crid=2NRBMHQW1QLW6")

headers = {
    "User-Agent": os.environ['HTTP_USER_AGENT'],
    "Accept-Language": os.environ['HTTP_ACCEPT_LANG']
}

response = requests.get(URL, headers=headers)
website_html = response.text

soup = BeautifulSoup(website_html, "lxml")
# print(soup.prettify())

product_title = soup.select_one("#productTitle").getText()

price_whole = soup.select_one(".a-price-whole").getText()
price_fraction = soup.select_one(".a-price-fraction").getText()
full_price = float(price_whole + price_fraction)

BUY_PRICE = 95

if full_price < BUY_PRICE:
    with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
        connection.starttls()
        connection.login(user=os.environ['MY_EMAIL'], password=os.environ['SMTP_PASSWORD'])

        connection.sendmail(
            from_addr=os.environ['MY_EMAIL'],
            to_addrs=os.environ['RECIPIENT_EMAIL'],
            msg=f"Subject:Amazon Price Alert!\n\n"
                f"{product_title.strip()}\n"
                f"now {full_price}\n"
                f"{URL}"
        )
