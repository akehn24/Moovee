import os
import pymongo
import random

#################################################################
# Moovee 
# Stores movies to watch via their genre. Has two specialty 
#  genres - Watched and Vetoed. 
#
# Imports:
#   os           - .env file
#   pymongo      - MongoDB database
#   random       - generates a random answer to a request
#################################################################

#################################################################
# Setting up the Moovee MongoDB
#
# Code provided by https://towardsdatascience.com
#################################################################
cluster = pymongo.MongoClient(os.getenv('MONGO'))
dtb = cluster["DCBots"]
mv = dtb["Moovee"]

movie_genres = []

#################################################################
# Helper functions to assist in parsing the user requests type
# obtain information to be stored in the Moovee database.
#
# Parameters:
#   movie_split     string with the event command removed
#################################################################
def get_movie_title(movie_split):
  # splits up the received user message into parts
  movie_title = movie_split.split(' to ',1)[0]
  return movie_title

def get_movie_genre(movie_split):
  # splits up the received user message into parts
  movie_genre = movie_split.split(' to ',1)[1]

  if movie_genre not in movie_genres:
    movie_genres.append(movie_genre)
  print(movie_genres)
  return movie_genre

def watched_or_vetoed(title):
  # checks the existing movie's genre
  if (mv.find({"movie title": title}, {"movie genre": {"$in": ["watched"]}})):
    return 1;
  elif (mv.find({"movie title": title}, {"movie genre": {"$in": ["vetoed"]}})):
    return 2;
  else:
    return 0


##################### Events ####################################
#################################################################
# Change a movie's genre to the new provided one.
#
# msg format: -change movie <movie title> to <movie genre>
#################################################################
async def change_movie(msg, message):
  # variables
  movie_split = msg.split('-change movie ',1)[1]
  title = get_movie_title(movie_split)
  genre = get_movie_genre(movie_split)

  if (watched_or_vetoed(title) == 1):
    await message.delete()
    # you've got a bug here if someone tries to change a watched movie to genre, if they want to watch it again!!
    # All change movies are hitting here instead of else???
    await message.channel.send("You've already got " + title + " on your watched list.")
  elif (watched_or_vetoed(title) == 2):
    await message.delete()
    await message.channel.send(title + " has been vetoed, sorry.")
  else:
    mv.update_one({"movie title": title}, {"$set":{"movie genre": genre}})
    await message.delete()
    await message.channel.send(title + "is already on the list. I'll update its genre to " + genre + "for you.") 

#################################################################
# Adds movies to the Moovee DB
#   Checks if the movie is already in the list under a different
#   genre. Updates the movie to the new genre given if so.
#
# msg format: -add movie <movie_title> to <movie_genre>
#################################################################
async def add_movie(msg, message):
  # variables
  movie_split = msg.split('-add movie ',1)[1]
  title = get_movie_title(movie_split)
  genre = get_movie_genre(movie_split)
  check_movie = {"movie title": title}

  if (mv.count_documents(check_movie) == 0):
    mv.insert_one({"movie title": title, "movie genre": genre})
    await message.delete()
    await message.channel.send("I added " + title + " to the " + genre + " genre, boss.")
  else:
    change_movie(msg, message)

#################################################################
# Change the movie's genre to 'watched'. To the user - this
#  effectively removes it from the movies to watch list.
#
# msg format: -we watched <movie_title>
#################################################################
async def movie_watched(msg, message):
  # variables
  movie_split = msg.split('-we watched ',1)[1]
  title = get_movie_title(movie_split)
  check_movie = {"movie title": title}

  if (mv.count_documents(check_movie) == 0):
    mv.insert_one({"movie title": title, "movie genre": "watched"})
    await message.delete()
    await message.channel.send("I've added " + title + " to your watched list.")
  else:
    mv.update_one({"movie title": title}, {"$set":{"movie genre": "watched"}})
    await message.delete()
    await message.channel.send("Awesome! I hope you liked it!")

#################################################################
# Provide random movies from the Moovee list.
#
# - don't include 'watched' and 'vetoed'
#
# msg format: -what should we watch?
#################################################################
'''async def get_random_movie(msg, message):
'''

#################################################################
# Delete a movie from the Moovee list. 
#
# msg format: -delete movie <movie's title>
#################################################################
async def delete_movie(msg, message):
  # variables
  movie_split = msg.split('-delete movie ',1)[1]
  title = get_movie_title(movie_split)
  
  # bugged - says delete() method doesn't exist?
  mv.delete({"movie title": title})
  await message.delete()
  await message.channel.send("I've removied (ha) " + title + " from the Movie List!")
    
#################################################################
# Provides list of movie genres in the Movie Night list. 
#
# msg format: -list genres
#################################################################
async def get_genres(message):
  # genre_list = {}
  
  await message.delete()
  await message.channel.send("__Movie Genres:__\n")
  for genre, value in movie_genres:
    print(genre + "\n")

  # for genre in genre_list:
    # await message.channel.send("__Here are your movie genres:__\n" + genre + "\n")
    # print("__Here are your movie genres:__\n" + genre + "\n")


#################################################################
# Provides list of movies in the provided genre from the Movie 
#  Night list. 
#
# msg format: -show me <movie genre>
#################################################################
async def get_movies_by_genre(msg, message):
  movie_split = msg.split('-show me ',1)[1]
  genre = get_movie_genre(movie_split)
  movie_list = []

  for movie in mv.find({}, {"movie": 1, "genre": 1}):
    if genre in movie:
      movie_list.append(movie)

  await message.delete()
  await message.channel.send("__Here are your movies in the " + genre + "list:__\n" + movie_list)


#################################################################
# Checks to see if the specified movie is already on the list. 
#
# msg format: -check movie <movie title>
#################################################################
'''async def check_movie(msg, message):
'''