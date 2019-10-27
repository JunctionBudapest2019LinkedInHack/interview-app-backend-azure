import logging
import azure.functions as func
import requests
import json

headers = {
            'Content-Type': 'application/json; charset:utf-8'
        }

getLinkedInDataUrl = 'https://junction-budapes-2019-tomaye.s3-eu-west-1.amazonaws.com/TomasYeMock.json'
getKeywordsFromLinkedInDataUrl = 'https://junctionbudapestfunctions3.azurewebsites.net/api/GetKeywordsFromLinkedInData?code=5x4MajA7or6MQBBQoxC6DEynOgamz8Ly2OcU61lki4NIYkbWauiIBg=='
getDescriptionFromKeywordsUrl = 'https://junctionbudapestfunctions3.azurewebsites.net/api/GetDescriptionFromKeywords?code=qDVJ3YaQdNbX5uFowK8UzbVEQ9CKD8P5p6/PvKem6UESbmcVO5fI8g=='
getAudioFromDescription = 'https://junctionbudapestfunctions3.azurewebsites.net/api/getAudioFromTextDescription?code=VNcJQoBUctRslPphXZZ9QEOoPjMT4bS8DdD2aZH2QEMTRXgi5NCkCQ=='


def main(req: func.HttpRequest) -> str:
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

    finalResponse = requests.post(url=getAudioFromDescription, json=description, headers=headers).text
    print('Final response = ')
    print(finalResponse)

    return finalResponse
