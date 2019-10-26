import logging
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Invoked Function for getting details ')
    return func.HttpResponse(
        "Hello world",
        status_code=400
    )

