import discord
import os
import dns
# import requests
# import json
import asyncio
import moovee as moovee
from keep_running import keep_running

#################################################################
# Moovee 
# Discord Bot that keeps a database of movies to watch. 
#
# Imports:
#   discord.py   - discord python api
#   os           - .env file
#   requests     - allows http reques to get data from APIs
#   json         - APIs return in json
#   random       - generates a random answer to a request
#   keep_running - file that keeps NerkBot running constantly
#################################################################

client = discord.Client()

#################################################################
# Initialization
#################################################################
@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))

#################################################################
#################################################################
#
# Events - Moovee Receives Message and Responds
#
# General Events:
#   Greeting                - says hello back
#   Testing                 - ping for activity
# 
# Movie Events:
#   Add Movie               - adds a movie to the list
#   We Watched              - changes a movie's genre to 'watched'
#   What Should We Watch    - provides a random movie from the list
#   Change Genre            - changes movie genre to the provided
#   Delete Movie            - removes the movie from the list
#   List Genres             - lists the movie genres available
#   List Movies             - lists the movies of a given genre
#   Check Movie             - checks if movie already exists in the list
#         
#################################################################
@client.event
async def on_message(message): 
  # ignore messages from Moovee
  if message.author == client.user:
    return
  msg = message.content

# Moovee Standard Greeting
  if msg.startswith('-hello moovee'):
    await message.channel.send('Hey there!')

# Moovee ping message
  if msg.startswith('-testing'):
    await message.channel.send('1 2 3')


####################### MOOVEE #############################
# Add movies to the Moovee DB
  # msg format: -add movie <movie_title> to <movie_genre>
  if msg.startswith('-add movie'):
    asyncio.create_task(moovee.add_movie(msg, message))

# Change movie's genre to 'watched'
  # msg format: -we watched <movie_title>
  if msg.startswith('-we watched'):
    asyncio.create_task(moovee.movie_watched(msg, message))

# Provides a random movie from the Moovee list
  # msg format: -what should we watch?

# Change movie's genre
  # msg format: -change movie <movie title> to <movie genre>
  if msg.startswith('-change movie'):
    asyncio.create_task(moovee.change_movie(msg, message))

# Delete movie from the Moovee list
  # msg format: -delete movie <movie's title>
  if msg.startswith('-delete movie'):
    asyncio.create_task(moovee.delete_movie(msg, message))

# Provides list of movie genres in the Moovee list
  # msg format: -list genres
  if msg.startswith('-list genres'):
    asyncio.create_task(moovee.get_genres(message))

# Provides list of movies in that genre in the Moovee list
  # msg format: -show me <movie genre>
  if msg.startswith('-show me'):
    asyncio.create_task(moovee.get_movies_by_genre(msg, message))

# Checks to see if the movie is already in the list
  # msg format: -check movie <movie title>

#################################################################
# Running NerkBot
#   Token provided by .env
#################################################################
keep_running()
client.run(os.getenv('TOKEN'))