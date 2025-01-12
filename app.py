from flask import Flask, render_template, request
from dotenv import load_dotenv
import requests
import os

app=Flask(__name__)

load_dotenv()

api_key=os.getenv('Spoonacular_API_KEY_2')

@app.route('/home',methods=["POST","GET"])
def home():
    if request.method=="POST":
        food_data=[]
        food_name=request.form.get('foodname')
        print(food_name)
        food_url=f"https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key}&query={food_name}"
        response=requests.get(food_url).json()
        # food_id=response['results'][0]['id']
        # food_title=response['results'][0]['title']
        for result in response.get('results',[]):
            food_id=result.get('id')
            food_image=result.get('image')
            food_title=result.get('title')
            print(f"food id: {food_id} and food title: {food_title}")
            food_data.append({
                'food_id':food_id,
                'food_image':food_image,
                'food_title':food_title
            })
        return render_template('index.html',food_data=food_data)
    else:
        return render_template('index.html')
    
@app.route('/food-details',methods=["POST","GET"])
def details():
    if request.method=="POST":

        ingredients_data=[]
        food_id=request.form.get('food_id')
        food_image=request.form.get('food_image')
        food_title=request.form.get('food_title')
        ingredients_url=f"https://api.spoonacular.com/recipes/{food_id}/ingredientWidget.json?apiKey={api_key}"
        ingredients_response=requests.get(ingredients_url).json()
        for ingredient_list in ingredients_response.get('ingredients',[]):
            ing_name = ingredient_list.get('name')
            ing_val = ingredient_list.get('amount', {}).get('us', {}).get('value')
            ing_units = ingredient_list.get('amount', {}).get('us', {}).get('unit')
            ingredients_data.append({
                'food_image':food_image,
                'ing_name':ing_name,
                'ing_val':ing_val,
                'ing_units':ing_units,
                'food_title':food_title
            })

        steps_data=[]
        steps_url=f"https://api.spoonacular.com/recipes/{food_id}/analyzedInstructions?apiKey={api_key}"
        response=requests.get(steps_url).json()
        # step=response[0]['steps'][0]['step']
        for each_step in response[0].get('steps',[]):
            steps=each_step.get('step')
            steps_data.append({
                'steps':steps
            })
        return render_template('details.html',ingredients_data=ingredients_data,steps_data=steps_data)

if __name__=="__main__":
    app.run(debug=True)