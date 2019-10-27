import logging
import requests
import time, uuid
from xml.etree import ElementTree
import azure.functions as func
from azure.storage.blob import BlockBlobService, PublicAccess
import json

headers = {
            'Content-Type': 'application/json; charset:utf-8',
        }

account_name = 'junctionbudapest2'
account_key = '1TUratXtvByc86ruuQ8ptxw51GUwnF1DpSZP4oMipSbONChihpLGPpCbar6y1SWANds5Ch+AUVLKrsyxpj3xKg=='
container_name = 'junction-2019-audio-descriptions'
block_blob_service = BlockBlobService(account_name=account_name, account_key=account_key)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Invoked function to transcribe text to file')
    description = req.get_json()['description']
    logging.info("Description = ")
    logging.info(description)
    soundFile = getSoundFromText(description)

    fileName = 'job_transcript_' + str(uuid.uuid4()) + '.wav'
    block_blob_service.create_blob_from_bytes(container_name, fileName, soundFile)
    soundFileURL = 'https://junctionbudapest2.blob.core.windows.net/' + container_name + '/' + fileName

    result = json.dumps({
        'soundFile': soundFileURL,
        'textDescription': description
    })

    return func.HttpResponse(result, mimetype='application/json', headers=headers)




def getSoundFromText(text):
    subscription_key = "2e27599545dc45289a620a8878b24793"
    app = TextToSpeech(subscription_key)
    token = app.get_token()
    return app.get_audio(token, text)


class TextToSpeech(object):

    def __init__(self, subscription_key):
        self.subscription_key = subscription_key
        self.timestr = time.strftime("%Y%m%d-%H%M")

    def get_token(self):
        fetch_token_url = "https://eastus.api.cognitive.microsoft.com/sts/v1.0/issuetoken"
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key
        }
        response = requests.post(fetch_token_url, headers=headers)
        return response.text

    def get_audio(self, token, text):
        base_url = 'https://eastus.tts.speech.microsoft.com/'
        path = 'cognitiveservices/v1'
        constructed_url = base_url + path
        headers = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
            'User-Agent': 'junctionbudapest'
        }
        xml_body = ElementTree.Element('speak', version='1.0')
        xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-us')
        voice = ElementTree.SubElement(xml_body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
        voice.set(
            'name', 'Microsoft Server Speech Text to Speech Voice (en-US, Guy24KRUS)')
        voice.text = text
        body = ElementTree.tostring(xml_body)

        response = requests.post(constructed_url, headers=headers, data=body)
        print('response  =')
        print(response)
        if response.status_code == 200:
            return response.content
        else:
            print("\nStatus code: " + str(response.status_code) +
                  "\nSomething went wrong. Check your subscription key and headers.\n")
            raise Exception("Something happened when calling speech to text -> Status code: " + str(response.status_code))

