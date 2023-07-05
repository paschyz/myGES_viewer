from config import *

from pymongo import MongoClient
import discord
def connect_to_mongodb(uri):
    client = MongoClient(uri)
    return client

def select_database(client, db_name):
    db = client[db_name]
    return db

def select_collection(db, collection_name):
    collection = db[collection_name]
    return collection

def find_documents(collection, filter=None):
    try:
        documents = collection.find(filter)
        print("yes")
        return documents
    except Exception as e:
        print(f"erreur: {str(e)} ")

def connect_to_mongo(uri):
    mongo_uri = uri
    client_mongo = connect_to_mongodb(mongo_uri)
    db_name = "myGES"
    collection_name_marks = "marks"
    collection_name_planning = "planning"
    collection_name_trombinoscope = "trombinoscope"
    collection_name_users = "users"
    db = select_database(client_mongo, db_name)

    collection_marks = select_collection(db, collection_name_marks)
    collection_planning = select_collection(db, collection_name_planning)
    collection_trombinoscope = select_collection(db, collection_name_trombinoscope)
    collection_users = select_collection(db, collection_name_users)
    
    return (
        client_mongo,
        collection_marks,
        collection_planning,
        collection_trombinoscope,
        collection_users
    )
    
async def display_marks(interaction, documents_marks):
    embeds = []
    for mark in documents_marks:
        document_id = mark.get("_id")
        user = mark.get("user")
        matiere = mark.get("matiere")
        intervenant = mark.get("intervenant")
        coef = mark.get("coef")
        ects = mark.get("ects")
        cc1 = mark.get("cc1")
        cc2 = mark.get("cc2")
        exam = mark.get("exam")

        message = f"Matière: {matiere}\n" \
                  f"Intervenant: {intervenant}\n" \
                  f"Coef.: {coef}\n" \
                  f"ECTS: {ects}\n" \
                  f"CC1: {cc1}\n" \
                  f"CC2: {cc2}\n" \
                  f"Exam: {exam}"

        embed = discord.Embed()
        embed.title = f"Matière: {matiere}\n"
        embed.set_footer(text=f"Intervenant: {intervenant}\n")
        embed.colour = discord.Color.blue()  # Set the color to blue

        embed.description = f"CC1: {cc1}\n" \
                            f"CC2: {cc2}\n" \
                            f"Exam: {exam}\n\n" \
                            f"Coef.: {coef}\n" \
                            f"ECTS: {ects}\n"
        embeds.append(embed)

    for embed in embeds:
        await interaction.channel.send(embed=embed)
        
async def verify_if_user_exists(interaction: discord.Interaction,collection):
    doc = collection.find_one({"user_discord_id": interaction.user.id})
    if doc is None:
        await interaction.response.send_message('No Data found for {}, try to use command \'/scrape\'!'.format(interaction.user.name))
        return False
    else:
        return True