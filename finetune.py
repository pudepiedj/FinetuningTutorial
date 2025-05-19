import os
import requests
import openai
from pprint import pprint

openai.api_key_path=".env"
# print("PATH = ",openai.api_key_path)
openai.api_key = os.getenv('OPENAI_API_KEY')
# print("KEY = ",openai.api_key)

#with open('openaiapikey.txt', 'r') as infile:
#    open_ai_api_key = infile.read()
#openai.api_key = open_ai_api_key

# this uploads the 
def file_upload(filename, purpose='fine-tune'):
    resp = openai.File.create(purpose=purpose, file=open(filename))
    pprint(resp)
    return resp


# lists the contents of a file using Pretty Print
def file_list():
    resp = openai.File.list()
    pprint(resp)

# does the heavy lifting interface with OpenAI; shouldn't need the literal key
def finetune_model(fileid, suffix, model='davinci'):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % openai.api_key}
    payload = {'training_file': fileid, 'model': model, 'suffix': suffix}
    resp = requests.request(method='POST', url='https://api.openai.com/v1/fine-tunes', json=payload, headers=header, timeout=45)
    pprint(resp.json())


def finetune_list():
    openai.api_key = os.getenv('OPENAI_API_KEY')
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % openai.api_key}
    resp = requests.request(method='GET', url='https://api.openai.com/v1/fine-tunes', headers=header, timeout=45)
    pprint(resp.json())


def finetune_events(ftid):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % openai.api_key}
    resp = requests.request(method='GET', url='https://api.openai.com/v1/fine-tunes/%s/events' % ftid, headers=header, timeout=45)    
    pprint(resp.json())


def finetune_get(ftid):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % openai.api_key}
    resp = requests.request(method='GET', url='https://api.openai.com/v1/fine-tunes/%s' % ftid, headers=header, timeout=45)    
    pprint(resp.json())


# How do we USE this finetuning to affect the behaviour of the chatbot?
# Essentially we take the prepared file consisting of PROMPT + COMPLETION from our synthesiser
# and we UPLOAD it to our personal account in OpenAI
# using the FUNCTION above called file_upload() with whatever our filename is
# and then we get a response including a file ID from OpenAI
# which we grab using the function filetune_model defined above

resp = file_upload('FinetuningTutorial/plots.jsonl')

# note that 'plot-generator' is the name of the uploaded file
# and it generates a model called "davinci:ft-plot_generator" (I think)

finetune_model(resp['id'], 'plot_generator', 'davinci')

# it appears that the "status":"pending" message means that your model has been uploaded
# but is now queued to be incorporated into the model
# apparently this can take many hours and involves costs
# that limit its availability to those with free access
# cf. https://community.openai.com/t/finetuning-not-working-pending-status/62488

models = openai.FineTune.list()
print(models)
# finetune_list()