import logging
import azure.functions as func
from azure.storage.blob import BlockBlobService
import json


output_container_name = 'junction-budapest-results'
account_name = 'junctionbudapest2'
account_key = '1TUratXtvByc86ruuQ8ptxw51GUwnF1DpSZP4oMipSbONChihpLGPpCbar6y1SWANds5Ch+AUVLKrsyxpj3xKg=='

blobService = BlockBlobService(account_name=account_name, account_key=account_key)

def main(req: func.HttpRequest) -> func.HttpResponse:
    name = req.params.get('name')
    fileName = getFileName(name)

    return func.HttpResponse(
             body=blobService.get_blob_to_text(output_container_name, fileName).content,
             status_code=200
        )




def getFileName(name):
    mapping = {
        'bernd': 'bernd_microsoft.json',
        'hanka': 'hanka.json',
        'lee': 'lee_microsoft.json',
        'martin': 'martin_microsoft.json',
        'lucie': 'lucie_microsoft.json',
        'tommy': 'tommy.json',
        'yuri': 'yuri.json'
    }

    if name in mapping.keys():
        return mapping[name]
    else:
        raise Exception('Unknown linked in user ' + name)
