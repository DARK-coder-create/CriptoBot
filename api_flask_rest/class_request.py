from flask_restful import Resource
from flask_restful import reqparse
from flask_restful import request

import requests
from bs4 import BeautifulSoup


class Request(Resource):
    def get(self):
        if request.args:
            answer = request.args.getlist("data")
        else:
            answer = []

        answer = [i.upper() for i in answer]

        req = requests.get("https://bitinfocharts.com/ru/crypto-kurs/")

        soup = BeautifulSoup(req.text, 'lxml')

        otvet = {}

        ad = soup.find('tbody')
        for i in soup.find_all("tr", attrs={'class': "ptr"}):
            for name in answer:
                if i.find("td", attrs={'data-val': name}):
                    otvet[name] = {}

                    tds = i.find_all("td")

                    otvet[name]["name"] = name.upper()
                    otvet[name]["price_usd"] = {}
                    otvet[name]["price_btc"] = {}
                    otvet[name]["capitalization"] = {}
                    otvet[name]["exchange_volume_is_24h"] = {}

                    otvet[name]["price_usd"]["today"] = tds[1].find("a").text
                    otvet[name]["price_usd"]["per_day"] = tds[1].find_all("span")[0].text
                    otvet[name]["price_usd"]["per_week"] = tds[1].find_all("span")[1].text

                    otvet[name]["price_btc"]["today"] = tds[2].find_all("span")[0].text
                    otvet[name]["price_btc"]["per_day"] = tds[2].find_all("span")[1].text
                    otvet[name]["price_btc"]["per_week"] = tds[2].find_all("span")[2].text

                    otvet[name]["capitalization"]["usd"] = tds[3].find_all("span")[0].text
                    otvet[name]["capitalization"]["btc"] = tds[3].find_all("span")[1].text

                    otvet[name]["exchange_volume_is_24h"]["value"] = " ".join(
                        [tds[4].find_all("span")[0].text, tds[4].find_all("span")[1].text])

                    otvet[name]["exchange_volume_is_24h"]["btc"] = " ".join(
                        [tds[4].find_all("span")[2].text.split("BTC")[0].strip(), "BTC"])
                    otvet[name]["exchange_volume_is_24h"]["usd"] = tds[4].find_all("span")[2].text.split("BTC")[
                        1].strip()

        return otvet, 200