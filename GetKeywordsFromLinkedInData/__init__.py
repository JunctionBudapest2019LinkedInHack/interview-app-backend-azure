import requests
import logging
import azure.functions as func
import json


def main(req: func.HttpRequest) -> str:
    logging.info('Invoked function to Extract keywords from LinkedIn profile')
    body = json.loads(req.get_body())[0]
    logging.info('Content =')
    logging.info(body)

    return extractKeyWords(body)



def getKeyPhrases(description):
    key = 'a0a9effb69214daaabbbb216bc0782d4'
    endpoint = 'https://junction2019.cognitiveservices.azure.com/text/analytics/v2.1/keyphrases'

    documents = {"documents": [
        {"id": "1", "language": "en",
         "text": description},
    ]}

    headers = {"Ocp-Apim-Subscription-Key": key}
    response = requests.post(endpoint, headers=headers, json=documents)
    return response.json()


def extractKeyWords(input_json) -> str:
    profile = {}

    # GENERAL
    description = input_json["general"]["description"]
    key_phrases = getKeyPhrases(description)
    general_info = input_json["general"]
    profile["general"] = []
    profile["general"].append({
        "fullName": general_info["fullName"],
        "headline": general_info["headline"],
        "company": general_info["company"],
        "location": general_info["location"],
        "keyPhrases": key_phrases['documents'][0]['keyPhrases']
    })

    # JOBS
    profile["jobs"] = []
    jobs = input_json["jobs"]
    for job in jobs:
        if job:
            description = job["description"]
            key_phrases = getKeyPhrases(description)
            profile["jobs"].append({
                "companyName": job["companyName"],
                "jobTitle": job["jobTitle"],
                "dateRange": job["dateRange"],
                "location": job["location"],
                "keyPhrases": key_phrases['documents'][0]['keyPhrases']
            })

    # SCHOOLS
    profile["schools"] = []
    schools = input_json["schools"]
    for school in schools:
        if school:
            description = school["description"]
            key_phrases = getKeyPhrases(description)
            key_phrases = key_phrases['documents'][0]['keyPhrases'] if key_phrases['documents'] else ""
            profile["schools"].append({
                "schoolName": school["schoolName"],
                "degree": school["degree"],
                "degreeSpec": school["degreeSpec"],
                "dateRange": school["dateRange"],
                "keyPhrases": key_phrases
            })

    profile["skills"] = []
    profile["skills"].append(input_json["skills"])

    return json.dumps(profile)
