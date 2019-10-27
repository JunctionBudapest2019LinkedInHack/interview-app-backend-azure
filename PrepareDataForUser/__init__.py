import logging
import random
import re
import datetime
import time, uuid
from xml.etree import ElementTree
import azure.functions as func
from azure.storage.blob import BlockBlobService
import json
import requests



account_name = 'junctionbudapest2'
account_key = '1TUratXtvByc86ruuQ8ptxw51GUwnF1DpSZP4oMipSbONChihpLGPpCbar6y1SWANds5Ch+AUVLKrsyxpj3xKg=='

audio_container_name = 'junction-2019-audio-descriptions'
input_container_name = 'mocked-linkedin-responses'
output_container_name = 'junction-budapest-results'

blobService = BlockBlobService(account_name=account_name, account_key=account_key)


def main(req: func.HttpRequest) -> func.HttpResponse:
    userName = req.params.get('name')
    fileName = getFileName(userName)

    linkedInData = json.loads(blobService.get_blob_to_text(input_container_name, fileName).content)
    logging.info('LinkedIn Data = ')
    logging.info(linkedInData)

    keywords = extractKeyWords(linkedInData)
    logging.info('Keywords')
    logging.info(keywords)

    description = magicFoo(json.dumps(keywords))
    logging.info('Description = ')
    logging.info(description)

    logging.info('Generating and storing sound')
    soundFileUrl = generateAndStoreSoundFromTextAndReturnUrl(description)

    result = json.dumps({
        'status': 'success',
        'description': description,
        'soundUrl': soundFileUrl
    })

    logging.info("")
    logging.info("Storing the pre computed result")
    blobService.create_blob_from_text(container_name=output_container_name, blob_name=fileName, text=result)

    return func.HttpResponse(result, status_code=200)



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


key = 'a0a9effb69214daaabbbb216bc0782d4'

endpoint = 'https://junction2019.cognitiveservices.azure.com/text/analytics/v2.1/keyphrases'


def getKeyPhrases(description):

    documents = {"documents": [
        {"id": "1", "language": "en",
         "text": description},
    ]}

    headers = {"Ocp-Apim-Subscription-Key": key}
    response = requests.post(endpoint, headers=headers, json=documents)
    return response.json()


def checkProperties(input_dict, output_dict):
    for property in output_dict:
        if input_dict.get(property):
            output_dict[property] = input_dict[property]
    key_phrases = getKeyPhrases(output_dict["description"])
    key_phrases = key_phrases['documents'][0]['keyPhrases'] if key_phrases['documents'] else ""
    return key_phrases


def extractKeyWords(json_input):
    profile = {}

    #GENERAL
    general_properties = {
        "fullName": "",
        "headline": "",
        "company": "",
        "location": "",
        "description": ""
    }

    general_info = json_input["general"]

    key_phrases = checkProperties(general_info, general_properties)
    profile["general"] = []
    profile["general"].append({
        "fullName": general_properties["fullName"],
        "headline": general_properties["headline"],
        "company": general_properties["company"],
        "location": general_properties["location"],
        "keyPhrases": key_phrases
    })


    #JOBS
    job_properties = {
        "companyName": "",
        "jobTitle": "",
        "dateRange": "",
        "location": "",
        "description": ""
    }

    profile["jobs"] = []
    jobs = json_input["jobs"]
    for job in jobs:
        if job:
            key_phrases = checkProperties(job, job_properties)
            profile["jobs"].append({
                "companyName": job_properties["companyName"],
                "jobTitle": job_properties["jobTitle"],
                "dateRange": job_properties["dateRange"],
                "location": job_properties["location"],
                "keyPhrases": key_phrases
            })


    # SCHOOLS
    school_properties = {
        "schoolName": "",
        "degree": "",
        "degreeSpec": "",
        "dateRange": "",
        "description": ""
    }

    profile["schools"] = []
    schools = json_input["schools"]
    for school in schools:
        if school:
            key_phrases = checkProperties(school, school_properties)
            profile["schools"].append({
                "schoolName": school_properties["schoolName"],
                "degree": school_properties["degree"],
                "degreeSpec": school_properties["degreeSpec"],
                "dateRange": school_properties["dateRange"],
                "keyPhrases": key_phrases
            })


    #SKILLS
    profile["skills"] = []
    profile["skills"].append(json_input["skills"])

    return profile








class tParamAlternative:
  def __init__(self):
    pass

def fixKey(key):
  new_key = key.lower().replace('-','_').replace(' ', '_').replace(',', '_')
  return new_key

def getKeys(text, strip=True):
  if text is None:
    return []

  matches = re.findall(r"\{[^\{\}]*\}", text)

  result = [(m[1:-1] if strip else m) for m in matches]
  return result

class tEntry:
  def __init__(self, text):
    self.template = self.fixKeys(text)

  def format(self, context):
    try:
      return self.template.format(**context)
    except Exception as e:
      return ""

  def keys(self):
    return getKeys(self.template)

  def fixKeys(self, text):
    new_text = text[:]
    for old_key in getKeys(text, False):
      new_text = new_text.replace(old_key, fixKey(old_key))

    return new_text

class tSet:
  def __init__(self, items):
    self.items = items

  def format(self, context):
    return random.choice(self.items).format(context)

  def keys(self):
    keys = []

    for item in self.items:
      keys.extend(item.keys())

    return keys

class tDocument:
  def __init__(self, sets):
    self.items = sets

  def keys(self):
    keys = []

    for item in self.items:
      keys.extend(item.keys())

    return set(keys)

  def format(self, context):
    text = [item.format(context) for item in self.items]

    return " ".join(text)

class Client:
  def __init__(self, document, context):
    self.document = document
    self.context = context

  def get(self):
    return self.document.format(self.context).replace("<br>", "\n   ")

def removeSeqDup(items):
  result = [items[0]]
  for item in items[1:]:
    if item != result[-1]:
      result.append(item)

  return result

def splitAt(items, delimiter):
  result = []
  chunk = []
  for item in items:
    if item == delimiter:
      result.append(chunk)
      chunk = []
    else:
      chunk.append(item)

  if chunk != []:
    result.append(chunk)

  return result

def buildDocumentTemplate(fname):
  FILE_HOSTING_PLATFORM_URL = 'https://junctionbudapest2.blob.core.windows.net/junction-junkies-2019-tomaye/'
  lines = []

  response = requests.get(FILE_HOSTING_PLATFORM_URL + fname)
  data = response.text.splitlines()
  for line in data:
      if line.startswith("*"):
        line = ''
        lines.append("<br>")
      else:
        lines.append(line.strip())

  lines = removeSeqDup(lines)
  # print(lines)

  chunks = splitAt(lines, '')
  # print(chunks)

  doc = tDocument([])
  for chunk in chunks:
    if chunk != []:
      entries = [tEntry(item) for item in chunk]
      tset = tSet(entries)
      doc.items.append(tset)

  return doc

def loadSrc(fname):
  with open(fname, "r") as read_file:
    return read_file.read()

def bind(foo, dst, dst_k):
  try:
    dst[dst_k] = foo()
  except Exception as e:
    # print("err")
    pass

def startYear(src):
  years = sorted(list(filter(lambda x: x > 1950, map(int, re.findall(r"\d{4}", src)))))
  return str(years[0])

def endYear(src):
  years = sorted(list(filter(lambda x: x > 1950, map(int, re.findall(r"\d{4}", src)))))
  return str(years[-1])

def yearSuffix(val):
  if val == 0:
    return "a few months"
  elif val == 1:
    return " a year"
  else:
    return str(val) + " years"

def yearsRange(src):
  years = sorted(list(filter(lambda x: x > 1950, map(int, re.findall(r"\d{4}", src)))))
  # print(years)
  val = years[-1] - years[0]

  return yearSuffix(val)

def startYears(src):
  year = sorted(list(filter(lambda x: x > 1950, map(int, re.findall(r"\d{4}", src)))))[0]
  return yearSuffix(datetime.datetime.now().year - year)

def endYears(src):
  year = sorted(list(filter(lambda x: x > 1950, map(int, re.findall(r"\d{4}", src)))))[-1]

  val = year - datetime.datetime.now().year
  return yearSuffix(val)

def getSubjects(skills, num):
  subjects = [x["name"] for x in random.sample(skills, k=num)]
  return ", ".join(subjects)

def getLanguage(skills, jobs):
  langs = ["C#", "Java", "C++", "HTML", "CSS", "JavaScript", "Python", "Haskell", "Bash", "SQL", "F#", "TypeScript", "Cotlin", "Racket", "R", "Julia", "Scheme", "Lisp", "Prolog"]
  subjects = set([x["name"] for x in skills])
  job_subj = []
  for job in jobs:
    job_subj.extend(x["keyPhrases"])

  subjs = subjects | job_subj
  lang = langs & subjs

  return str(random.choice(lang))
  # return str(random.choice(subjects))

def getSoftSkill(skills):
  sskills = ["project management", "interpersonal skills", "project lead"]
  return str(random.choice(sskills))

def getSubject(skills, order = None):
  if order is None:
    return str(random.choice(skills)["name"])
  else:
    return str(skills[order]["name"])

def getTask(jobs):
  return str(random.choice(jobs[0]["keyPhrases"]))

def qualification(jobs, num):
  return str(random.choice(jobs[-num]["keyPhrases"]))

def jobSkill(jobs, i, seq):
  return jobs[i]["keyPhrases"][-seq]

def fuseKeys(src, dst, text):
  general = src['general']
  jobs = src['jobs']
  skills = src['skills'][0]
  # print(random.choice(skills)["name"])
  schools = src['schools']
  # print(endYears(schools[0]["dateRange"]))
  print(yearsRange(jobs[-1]["dateRange"]))
  print(jobs[-1]["dateRange"])

  # bind = lambda src_k, dst_k: tryFill(general, jobs, skills, schools, src_k, dst_k, dst)

  # bind(general, "", dst, "")
  # bind(general, "", dst, 'achievement_1')
  bind(lambda: getSubject(skills, 0), dst, 'achievement_1')
  bind(lambda: schools[-1]["degree"], dst, 'edu1_qualification')
  bind(lambda: schools[-1]["degreeSpec"], dst, 'edu1_subject')
  bind(lambda: schools[-1]["degreeSpec"], dst, 'edu1_subject_1')
  bind(lambda: yearsRange(schools[-1]["dateRange"]), dst, 'edu1_years')
  bind(lambda: getSubject(skills, 0), dst, 'edu2_subject')
  bind(lambda: getSubject(skills, 1), dst, 'edu2_subject_1')
  bind(lambda: getSubject(skills, 2), dst, 'edu2_subject_2')
  bind(lambda: getSubject(skills, 3), dst, 'edu2_subject_3')
  bind(lambda: schools[-3]["degree"], dst, 'edu3_qualification')
  bind(lambda: getSubjects(skills, 3), dst, 'edu3_subject_1_2_3')
  bind(lambda: startYear(schools[-3]["dateRange"]), dst, 'edu3_year')
  bind(lambda: schools[-1]["schoolName"], dst, 'edu_organisation_1')
  bind(lambda: yearsRange(schools[-1]["dateRange"]), dst, 'edu_organisation_1_years')
  bind(lambda: schools[-2]["schoolName"], dst, 'edu_organisation_2')
  bind(lambda: schools[-3]["schoolName"], dst, 'edu_organisation_3')
  bind(lambda: schools[0]["schoolName"], dst, 'edu_organisation_c')
  bind(lambda: endYear(schools[0]["dateRange"]), dst, 'educ_end_year')
  bind(lambda: getSubjects(skills, 3), dst, 'educ_subject_1_2_3')
  bind(lambda: endYear(schools[0]["dateRange"]), dst, 'end_year_c')
  bind(lambda: endYears(schools[0]["dateRange"]), dst, 'end_years_c')
  bind(lambda: getLanguage(skills), dst, 'language_1')
  bind(lambda: getLanguage(skills), dst, 'language_2')
  bind(lambda: getLanguage(skills), dst, 'language_3')
  bind(lambda: schools[-1]["degree"], dst, 'qualification_1')
  bind(lambda: schools[-3]["degree"], dst, 'qualification_3')
  bind(lambda: getSubject(skills, 0), dst, 'skill_1')
  bind(lambda: getSubject(skills, 1), dst, 'skill_2')
  bind(lambda: getSubject(skills, 2), dst, 'skill_3')
  bind(lambda: getSubject(skills, 3), dst, 'skill_4')
  bind(lambda: getSoftSkill(skills), dst, 'soft_skill_1')
  bind(lambda: getSoftSkill(skills), dst, 'soft_skill_2')
  bind(lambda: getSoftSkill(skills), dst, 'soft_skill_3')
  bind(lambda: schools[-1]["degree"], dst, 'start_achievement')
  bind(lambda: yearsRange(text), dst, 'start_few')
  bind(lambda: schools[-1]["degreeSpec"], dst, 'start_subject')
  bind(lambda: getTask(jobs), dst, 'start_task_1')
  bind(lambda: getTask(jobs), dst, 'start_task_2')
  bind(lambda: getTask(jobs), dst, 'start_task_3')
  bind(lambda: jobs[-1]["jobTitle"], dst, 'start_title')
  bind(lambda: jobs[-1]["companyName"], dst, 'start_work_place')
  bind(lambda: startYear(text), dst, 'start_year')
  bind(lambda: startYears(text), dst, 'start_years')
  bind(lambda: getSubject(skills, 0), dst, 'subject_1')
  bind(lambda: getSubjects(skills, 3), dst, 'subject_1_2_3')
  bind(lambda: getSubject(skills, 1), dst, 'subject_2')
  bind(lambda: getSubject(skills, 2), dst, 'subject_3')
  bind(lambda: getTask(jobs), dst, 'task_1')
  bind(lambda: getTask(jobs), dst, 'task_2')
  bind(lambda: getTask(jobs), dst, 'task_3')
  bind(lambda: jobs[-1]["jobTitle"], dst, 'title_1')
  bind(lambda: jobs[-2]["jobTitle"], dst, 'title_2')
  bind(lambda: jobs[0]["jobTitle"], dst, 'title_c')
  bind(lambda: startYear(jobs[-1]["dateRange"]), dst, 'work1_start_year')
  bind(lambda: jobSkill(jobs, 0, 0), dst, 'work1_subject')
  bind(lambda: jobSkill(jobs, 1, 0), dst, 'work2_skill_1')
  bind(lambda: jobSkill(jobs, 1, 1), dst, 'work2_skill_2')
  bind(lambda: jobSkill(jobs, 1, 2), dst, 'work2_skill_3')
  bind(lambda: startYear(jobs[-2]["dateRange"]), dst, 'work2_year')
  bind(lambda: yearsRange(jobs[-2]["dateRange"]), dst, 'work2_years')
  bind(lambda: yearsRange(jobs[-1]["dateRange"]), dst, 'work_place1_years')
  bind(lambda: jobs[-1]["companyName"], dst, 'work_place_1')
  bind(lambda: jobs[-2]["companyName"], dst, 'work_place_2')
  bind(lambda: jobs[0]["companyName"], dst, 'work_place_c')
  bind(lambda: getSubject(skills), dst, 'work_subject_1')
  bind(lambda: startYear(jobs[-1]["dateRange"]), dst, 'work_year_1')
  bind(lambda: yearsRange(jobs[-1]["dateRange"]), dst, 'work_years_1')
  bind(lambda: startYears(jobs[0]["dateRange"]), dst, 'work_years_c')

  # print(schools)

def chooseTemplate(context):
  templates = []
  if ("work_place_1" in context) or ("work_place_c" in context):
    templates = ["blended1.txt", "carreer1.txt", "carreer2.txt"]
  else:
    templates = ["education1.txt", "education2.txt"]

  return random.choice(templates)

def magicFoo(json_context):
  src = json.loads(json_context)
  context = dict()
  fuseKeys(src, context, json_context)

  doc = buildDocumentTemplate(chooseTemplate(context))

  cl = Client(doc, context)
  return cl.get().replace("’", "")



def generateAndStoreSoundFromTextAndReturnUrl(description) -> str:
    soundFile = getSoundFromText(description)
    fileName = 'job_transcript_' + str(uuid.uuid4()) + '.wav'
    blobService.create_blob_from_bytes(audio_container_name, fileName, soundFile)
    return 'https://junctionbudapest2.blob.core.windows.net/' + audio_container_name + '/' + fileName



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

