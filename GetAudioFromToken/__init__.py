import logging
import azure.functions as func
import requests
import json

headers = {
            'Content-Type': 'application/json; charset:utf-8'
        }

getLinkedInDataUrl = 'https://junction-budapes-2019-tomaye.s3-eu-west-1.amazonaws.com/TomasYeMock.json'
getKeywordsFromLinkedInDataUrl = 'https://junctionbudapest.azurewebsites.net/api/GetKeywordsFromLinkedInData?code=b/DEa4NacEHn0ZcUyDci3Kap1R6bVGTDFVNkdfEcepYPsb7jyxSDEQ=='
getDescriptionFromKeywordsUrl = 'https://junctionbudapest.azurewebsites.net/api/GetDescriptionFromKeywords?code=pM1Y/934iOd8ZjuGaBqtlUBDUoyDwYXjauVRI04k9d8/BZXr4kn3wg=='


def main(req: func.HttpRequest) -> str:
    logging.info('Invoked Function for getting details ')
    linkedInData = requests.get(getLinkedInDataUrl).json()

    print('LinkedInData = ')
    print(linkedInData)

    keywords = requests.post(url=getKeywordsFromLinkedInDataUrl, json=linkedInData, headers=headers).json()
    print('Keywords = ')
    print(keywords)

    description = requests.post(url=getDescriptionFromKeywordsUrl, json=keywords, headers=headers).text
    print('Keywords = ')
    print(description)

    return description