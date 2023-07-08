from config import *
import os

import base64
import aiohttp
from pymongo import MongoClient
import discord
import hashlib

password_salt = os.getenv("PASSWORD_SALT")


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
    collection_trombinoscope = select_collection(
        db, collection_name_trombinoscope)
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
        matiere = mark.get("matiere")
        intervenant = mark.get("intervenant")
        coef = mark.get("coef")
        ects = mark.get("ects")
        cc1 = mark.get("cc1")
        cc2 = mark.get("cc2")
        exam = mark.get("exam")

        embed = discord.Embed()
        embed.title = f"Notes: {matiere}\n"
        embed.set_footer(text=f"Intervenant: {intervenant}\n")
        embed.colour = discord.Color.blue()  # Set the color to blue

        embed.add_field(name="CC1", value=cc1, inline=True)
        embed.add_field(name="CC2", value=cc2, inline=True)
        embed.add_field(name="Exam", value=exam, inline=True)
        embed.add_field(name="Coef.", value=coef, inline=True)
        embed.add_field(name="ECTS", value=ects, inline=True)
        embeds.append(embed)

    for embed in embeds:
        await interaction.channel.send(embed=embed)


async def display_planning(interaction, documents_planning):
    embeds = []
    for planning in documents_planning:
        duree = planning.get("duration")
        matiere = planning.get("matiere")
        intervenant = planning.get("intervenant")
        salle = planning.get("salle")
        type = planning.get("type")
        modalite = planning.get("modalite")
        date = planning.get("date")

        embed = discord.Embed()
        embed.title = f"{type}: {matiere}"
        embed.set_footer(text=f"Intervenant: {intervenant}")
        embed.colour = discord.Color.blue()

        embed.add_field(name="Durée", value=duree, inline=True)
        embed.add_field(name="Date", value=date, inline=True)
        embed.add_field(name="Salle", value=salle, inline=True)
        embed.add_field(name="Modalité", value=modalite, inline=True)

        embeds.append(embed)

    for embed in embeds:
        await interaction.channel.send(embed=embed)


async def display_trombinoscope(interaction, documents_trombinoscope):
    embeds = []
    for trombinoscope in documents_trombinoscope:
        nom = trombinoscope.get("nom")
        img_url = trombinoscope.get("img_url")
        user_discord_id = trombinoscope.get("user_discord_id")
        user = trombinoscope.get("user")
        categorie = trombinoscope.get("categorie")
        annee = trombinoscope.get("annee")
        embed = discord.Embed()
        embed.title = nom
        embed.set_footer(text=f"{annee}")
        embed.set_image(url=img_url)
        embed.colour = discord.Color.blue()
        embed.add_field(name="",
                        value=categorie, inline=False)
        embeds.append(embed)

    for embed in embeds:
        await interaction.channel.send(embed=embed)


async def perform_login(interaction: discord.Interaction, username: str, password: str):
    login_url = "https://authentication.kordis.fr/oauth/authorize?response_type=token&client_id=skolae-app"

    credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
    headers = {"Authorization": f"Basic {credentials}"}

    async with aiohttp.ClientSession() as session:
        async with session.get(login_url, headers=headers, allow_redirects=False) as response:
            # Check the response status code
            if response.status == 302:
                salted_password = password+password_salt
                # Define the document to insert or update
                base64_password = base64.b64encode(salted_password.encode())
                # Convert the encoded bytes to a string
                encoded_password = base64_password.decode()
                document = {
                    "username": username,
                    "password": encoded_password,
                    "username_discord": interaction.user.name,
                    "user_discord_id": interaction.user.id,
                }
                # decoded_password = hashed_password.hexdigest()
                # print("Decoded password:", decoded_password)

                # Define the query to find the document
                query = {"user_discord_id": interaction.user.id}

                # Perform the update operation
                result = collection_users.update_one(
                    query, {"$set": document}, upsert=True)

                if result.upserted_id is not None:
                    # Document inserted
                    print("Document inserted:", result.upserted_id)
                else:
                    # Document updated
                    print("Document updated:", query)

                await interaction.response.send_message("Connexion réussie ! Vous avez maintenant accès à la commande '/scrape' !", ephemeral=True)
            else:
                await interaction.response.send_message("Connexion échouée. Veuillez réessayer", ephemeral=True)


async def verify_if_user_exists(interaction: discord.Interaction, collection):
    doc = collection.find_one({"user_discord_id": interaction.user.id})
    if doc is None:
        await interaction.response.send_message('No Data found for {}, try to use command \'/scrape\'!'.format(interaction.user.name))
        return False
    else:
        return True
