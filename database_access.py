from weakref import proxy
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import os
from nanoid import generate


#Grabs the environment file
load_dotenv(find_dotenv())
MONGODB_CONNECTION = os.environ.get("MONGODB_CONNECTION")

#Connect to the database
client = MongoClient(MONGODB_CONNECTION)
db = client.links
collection = db.links

def find_by_short(short_link):
    return collection.find_one({"shortLink": short_link})


def insert_new_link(long_link):
    #Check if the link has already been shortened and return the element if it has
    validation = find_by_long(long_link)
    if validation is not None:
        return validation
    #If not, generate a new short link and add a new element
    short_link = generate_short_link()
    element_id = collection.insert_one({
        "longLink": long_link,
        "shortLink": short_link
        }).inserted_id
    
    return collection.find_one({"_id": element_id})
    

def find_by_long(long_link):
    return collection.find_one({"longLink": long_link})
    
    
def find_by_id(element_id):
    return collection.find_one({"_id": element_id})


def generate_short_link():
    return generate(size=6)


