from flask import Flask
from threading import Thread

#################################################################
# Keep Running 
# Turns Moovee into a Repl.it server so it can run in the 
#  background. 
#
# Code from Repl.it
# Imports:
#  Flask  - web server
#  Thread - running on a serparate thread from Moovee
#################################################################

app = Flask('')

@app.route('/')
def home():
  return "Running..."

def run():
  app.run(host='0.0.0.0', port=8080)

def keep_running():
  t = Thread(target=run)
  t.start()