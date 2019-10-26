import logging
import json
import azure.functions as func


def main(req: func.HttpRequest) -> str:
    logging.info('Invoked function for creating description from keywords')
    body = json.loads(req.get_body())

    logging.info('Doing some parsing magic with input = ')
    logging.info(body)

    return "Sample text: You stink!"
