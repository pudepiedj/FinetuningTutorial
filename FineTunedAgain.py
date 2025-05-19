import os
import openai

openai.api_key_path = '.env'
openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.Completion.create(
  model="davinci:ft-personal:plot-generator-2023-02-28-21-34-17",
  prompt="Genre: sci fi\nPlace: Mars\nPeriod: 2078\nModifier: Dog training in space\nOwnername: Susan\nDogname: Zachary\n\nPLOT OUTLINE:",
  temperature=0.7,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)
print(response)