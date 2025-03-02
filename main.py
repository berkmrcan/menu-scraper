from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
from openai import OpenAI
import os
import json
from collections import defaultdict

load_dotenv()  # Loads variables from .env into environment

API_KEY = os.getenv("OPENAI_API_KEY")
DEBUG = os.getenv("DEBUG")



url = "https://yemekhane.bogazici.edu.tr/"

response = requests.get(url=url, verify=False)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    lunch = soup.find(id="block-views-yemek-block")
    dinner = soup.find(id="block-views-yemek-block-1")
    if lunch and dinner:
        meal_items = {
            "Öğle Yemeği": defaultdict(list),
            "Akşam Yemeği": defaultdict(list)
        }
        for time, key in zip((lunch,dinner),("Öğle Yemeği","Akşam Yemeği")):
            
            categories = {
                "views-field-field-anaa-yemek": "Ana Yemek", 
                "views-field-field-yardimciyemek": "Yardımcı Yemek", 
            }
            
            
            for category in categories.keys():
                meals = time.find_all("div", class_=category)
                for meal in meals:
                    meal_names = meal.find_all("a")
                    for meal_name in meal_names:
                        if meal_name:
                            meal_items[key][categories[category]].append(meal_name.text.strip())

            # Print or process extracted meal names
        meal_data = json.dumps(meal_items, ensure_ascii=False)


    client = OpenAI()
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": f"""Analyze today meal data and tell me if 'Öğle Yemeği' and 'Akşam Yemeği' contains high protein or not.
         Examples: Mantar Soslu Tavuk, Kabak Beğendi are high protein. Yeşil Fasulye, Pizza are low protein. 
         If not sure if it is high or not, like Hasanpaşa Köfte, return YES if the Yardımcı Yemek contains any complex carbohydrate source like Bulgur. 
         Here is the today meal data: {meal_data}. Return a JSON response like: {{'Öğle Yemeği': 'YES/NO', 'Akşam Yemeği': 'YES/NO'}}"""}
    ]
    )

    print(completion.choices[0].message)


