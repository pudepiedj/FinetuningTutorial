# trained finetuning model
import os
import openai

openai.api_key_path = "~/edsil/openai-store/.env"
openai.api_key = os.getenv("OPENAI_API_KEY")

def gpt_ft(prompt="Genre: historical novel\nPlace: Rome\nPeriod: The ancient world\nModifier: Dog training\nOwnername: Susan\nDogname: Hugo\n\nPLOT OUTLINE:\n\n",model='davinci:ft-personal:plot-generator-2023-02-28-21-34-17', response_length=512,temperature=0.9, top_p=1, frequency_penalty=0, presence_penalty=0,start_text='', restart_text='', stop_seq=[]):
            response = openai.Completion.create(
              model=model,
              prompt=prompt,
              temperature=temperature,
              max_tokens=256,
              top_p=top_p,
              frequency_penalty=frequency_penalty,
              presence_penalty=presence_penalty,
              start_text=start_text,
              restart_text=restart_text,
              stop_seq=stop_seq,
            )
            print(gpt_ft.response['choices'][0]['text'])

if __name__ == '__main()__':
    gpt_ft()