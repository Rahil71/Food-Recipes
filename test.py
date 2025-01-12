# This file is just for API checking

import requests
from dotenv import load_dotenv
import os

load_dotenv()

apikey=os.getenv('Spoonacular_API_KEY_2')

steps_url=f"https://api.spoonacular.com/recipes/655098/analyzedInstructions?apiKey={apikey}"

response=requests.get(steps_url).json()

# step=response[0]['steps'][0]['step']

for each_step in response[0].get('steps',[]):
    steps=each_step.get('step')
    print(steps)