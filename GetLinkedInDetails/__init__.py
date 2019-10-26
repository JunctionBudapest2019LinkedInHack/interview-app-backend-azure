import logging
import json

import azure.functions as func


def main(req: func.HttpRequest) -> str:


    logging.info('Get LinkedIn Data function has been called')
    with open('./GetLinkedInDetails/TommyResponseJson.json') as json_file:
        data = json.load(json_file)
        logging.info('JSON = ')
        logging.info(data)
        return json.dumps(data)

