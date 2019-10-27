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
getAudioFromDescription = 'https://junctionbudapestfunctions3.azurewebsites.net/api/getAudioFromTextDescription?code=VNcJQoBUctRslPphXZZ9QEOoPjMT4bS8DdD2aZH2QEMTRXgi5NCkCQ=='


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Invoked Function for getting details ')
    linkedInData = requests.get(getLinkedInDataUrl).json()

    print('LinkedInData = ')
    print(linkedInData)

    keywords = requests.post(url=getKeywordsFromLinkedInDataUrl, json=linkedInData, headers=headers).json()
    print('Keywords = ')
    print(keywords)

    description = requests.post(url=getDescriptionFromKeywordsUrl, json=keywords, headers=headers).json()
    print('Description = ')
    print(description)

    finalResponse = requests.post(url=getDescriptionFromKeywordsUrl, json=description, headers=headers).text
    print('Final response = ')
    print(finalResponse)

    return func.HttpResponse(body=finalResponse, headers=headers)