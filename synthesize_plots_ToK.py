import os # just need this for the API_KEY security
import openai
from time import time,sleep
from uuid import uuid4


def open_file(filepath):
    # print("Current filepath ... ",filepath)
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


openai.api_key_path="/Users/edsil/openai-store/.env"
openai.api_key = os.getenv('OPENAI_API_KEY')
# openai.api_key = open_file('openaiapikey.txt')

q_prefixes = [
    'How easy or difficult is it',
    'What difference does it make',
    'What difficulties are',
    'Is it possible',
]

q_spheres = [
    'to avoid indecision in',
    'to establish facts in',
    'to be certain of',
    'to identify bias in',
]

q_aoks = [
    'the difference between fact and opinion',
    'natural science',
    'mathematics',
    'the arts',
    'languages',
    'the humanities',
    'general knowledge',
]

q_choices = [
    'the humanities and any one other area of knowledge',
    'the arts and any one other area of knowledge',
    'languages and any one other area of knowledge',
    'any two areas of knowledge',
    'between the natural sciences and the arts',
    'any area of knowledge',
]

# March 1st, 2023 OpenAI released gpt-3.5-turbo-0301 at 10% of the text-davinci-003 cost
def gpt3_completion(prompt, model='gpt-3.5-turbo-0301', temp=1.0, top_p=1.0, tokens=1000, freq_pen=0.0, pres_pen=0.0, stop=['asdfasdf', 'asdasdf']):
    max_retry = 1
    retry = 0
    prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
    while True:
        try:
            response = openai.Completion.create(
                model=model,
                prompt=prompt,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop)
            text = response['choices'][0]['text'].strip()
            print('completion = ',text)
            # text = re.sub('\s+', ' ', text)
            filename = '%s_gpt3.txt' % time()
            save_file('/Users/edsil/openai-store/FinetuningTutorial/gpt3-logs/%s' % filename, prompt + '\n\n==========\n\n' + text)
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return "GPT3 error: %s" % oops
            print('Error communicating with OpenAI:', oops)
            sleep(1)


if __name__ == '__main__':
    count = 0
    for q_prefix in q_prefixes:        # ideally we would randomise these rather than run them sequentially
        for q_sphere in q_spheres:      # of course we don't need to use all of them
            for q_aok in q_aoks:
                for q_choice in q_choices:
                    count += 1
                    prompt = open_file('FinetuningTutorial/prompt.txt')
                    prompt = prompt.replace('<<q_prefix>>', q_prefix)
                    prompt = prompt.replace('<<q_sphere>>', q_sphere)
                    prompt = prompt.replace('<<q_aok>>', q_aok)
                    prompt = prompt.replace('<<q_choice>>', q_choice)
                    prompt = prompt.replace('<<UUID>>', str(uuid4()))
                    print('\nThis is the initial prompt provided to the chatbot ...\n\n', prompt)
                    completion = gpt3_completion(prompt)
                    # completion = "just testing"
                    outprompt = 'Prefix: %s\nSphere: %s\nAOK: %s\nChoice: %s\n\nTOK ESSAY QUESTION: ' % (q_sphere, q_prefix, q_aok, q_choice)
                    filename = (q_prefix + q_sphere + q_aok + q_choice).replace(' ','').replace('&','') + '%s.txt' % time()
                    save_file('/Users/edsil/openai-store/FinetuningTutorial/prompts_tok/%s' % filename, outprompt)
                    save_file('/Users/edsil/openai-store/FinetuningTutorial/completions_tok/%s' % filename, completion)
                    #print('\n\n', outprompt)
                    #print('\n\n', completion)
                    if count > 5:
                        exit()
    #print(count)