import logging
import azure.functions as func
import requests

getLinkedInDataUrl = 'https://junctionbudapest.azurewebsites.net/api/GetLinkedInDetails?code=UkMZMr9qcjxgvPgTF2bVViTfl8vdFqu5nRreUbjim0UwBR8x7df5HA=='

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Invoked Function for getting details ')
    response = requests.get(getLinkedInDataUrl)
    print('Response = ')
    print(response.text)



    return func.HttpResponse(
        "Hello world",
        status_code=400
    )

