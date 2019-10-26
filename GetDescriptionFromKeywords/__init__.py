import logging

import azure.functions as func


def main(req: func.HttpRequest) -> str:
    logging.info('Invoked function for parsing template')    
    return "Getting text from template"
