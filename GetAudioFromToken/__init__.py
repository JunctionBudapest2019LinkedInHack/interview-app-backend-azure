import logging
import azure.functions as func
import requests
import json

headers = {
            'Content-Type': 'application/json; charset:utf-8'
        }

# getLinkedInDataUrl = 'https://junctionbudapest.azurewebsites.net/api/GetLinkedInDetails?code=UkMZMr9qcjxgvPgTF2bVViTfl8vdFqu5nRreUbjim0UwBR8x7df5HA=='
getLinkedInDataUrl = 'http://localhost:7071/api/GetLinkedInDetails'
getKeywordsFromLinkedInDataUrl = 'https://junctionbudapest.azurewebsites.net/api/GetKeywordsFromLinkedInData?code=b/DEa4NacEHn0ZcUyDci3Kap1R6bVGTDFVNkdfEcepYPsb7jyxSDEQ=='


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Invoked Function for getting details ')
    linkedInData = requests.get(getLinkedInDataUrl)

    print('LinkedInData = ')
    data = linkedInData.json()
    print(data)
    print(type(data))


    keywords = requests.post(url=getKeywordsFromLinkedInDataUrl, json=data, headers=headers)
    print('Keywords = ')
    print(keywords)



    return keywords.text