from django.db import models
import google.generativeai as genai
import json

# Create your models here.
# FILE: myapp/models.py
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
# MongoDB connection details
uri = 'mongodb+srv://andre:WangoTango238@tick-my-way.fiy3g.mongodb.net/?retryWrites=true&w=majority&appName=tick-my-way'  # Replace with your actual MongoDB URI
google_api_key = 'AIzaSyDAEx9XaJEz_eBc-JrWMexdWZLOh5gRqR4'
genai.configure(api_key=google_api_key)
model = genai.GenerativeModel("gemini-1.5-flash")


client = MongoClient(uri, server_api=ServerApi('1'))
db = client['SITE_DETAILS']
users_collection = db['Users']
lookup_collection = db['Institute_Lookup']
map_collection = db['Paths']

# Example function to insert a user
def insert_user(email, password, role, username, institute):
    user = {
        "email": email,
        "password": password,
        "role": role,
        "username": username,
        "institute": institute,
        "platinum": 100,
        "experience": 20,
        "level": 2,
        "login_dates": [],
        "created_at": datetime.utcnow()
    }
    users_collection.insert_one(user)

# Example function to find a user by email
def find_user(email):
    return users_collection.find_one({"email": email})

# Example function to insert an institute
def insert_institute(name, address):
    institute = {
        "name": name,
        "address": address,
        "created_at": datetime.utcnow()
    }
    lookup_collection.insert_one(institute)

# Example function to find an institute
def find_institute(name):
    return lookup_collection.find_one({"name": name})

# Function to add a login date
def add_login_date(email):
    login_date = datetime.utcnow().strftime('%Y-%m-%d')
    users_collection.update_one(
        {"email": email},
        {"$addToSet": {"login_dates": login_date}}
    )

# Function to get login dates
def get_login_dates(email):
    user = find_user(email)
    return user.get('login_dates', []) if user else []


def generate_and_store_content(topic, count, user_email='andredsouza256@gmail.com'):   #temporarily hardcoded email
    prompt = f"You are an AI that generates a MongoDB-style array of elements for the topic {topic}. Each element must contain a title, description, difficulty (easy, medium, hard), and status (done or not done, default=not_done).\nGenerate {count} items in the required format."
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    # Print the raw response text for debugging
    print("Raw response text:", response.text)

    # Remove the surrounding markdown formatting
    raw_text = response.text.strip('```json\n').strip('\n```')

    # Parse the JSON response and store it in a list
    try:
        temp_list = json.loads(raw_text)
        # Print the list
        print(temp_list)

        # Create a single document with the list of items
        for item in temp_list:
            item['status'] = 'not_done'

        document = {
            "user_email": user_email,
            "topic": topic,
            "generated_items": temp_list,
            "created_at": datetime.utcnow()
        }

        # Insert the document into the collection
        map_collection.insert_one(document)
        print(f"Inserted document with {len(temp_list)} items into the collection.")
    except json.JSONDecodeError as e:
        print("Failed to decode JSON:", e)

def get_generated_items(user_email='andredsouza256@gmail.com', q_topic=None):  #temporarily hardcoded email
    documents = map_collection.find({"user_email": user_email, "topic" : q_topic}, {"_id": 0, "generated_items": 1})
    generated_items = []
    for doc in documents:
        generated_items.extend(doc.get('generated_items', []))
    return generated_items
