import logging
import azure.functions as func
import requests
import json

headers = {
            'Content-Type': 'application/json; charset:utf-8'
        }

getLinkedInDataUrl = 'https://junction-budapes-2019-tomaye.s3-eu-west-1.amazonaws.com/TomasYeMock.json'
getKeywordsFromLinkedInDataUrl = 'https://junctionbudapest.azurewebsites.net/api/GetKeywordsFromLinkedInData?code=b/DEa4NacEHn0ZcUyDci3Kap1R6bVGTDFVNkdfEcepYPsb7jyxSDEQ=='


def main(req: func.HttpRequest) -> str:
    logging.info('Invoked Function for getting details ')
    linkedInData = requests.get(getLinkedInDataUrl).json()

    print('LinkedInData = ')
    print(linkedInData)


    keywords = requests.post(url=getKeywordsFromLinkedInDataUrl, json=linkedInData, headers=headers).text
    print('Keywords = ')
    print(keywords)
    print(type(keywords))

    return keywords