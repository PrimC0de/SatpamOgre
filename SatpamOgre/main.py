import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

sad_words = ["kon", "ajg" , "asw",
"tai","mmk", "ppk", "ppq", "tod", "tol", "mmq",
"KON", "KOON", "AJG", "TAI", "TOD", "TOL", "MMQ",
"PPK", "PPQ", "ASW", "BABI", "babi", "anjing", "bgst", "bangsat"]

starter_encouragements = ["🚓🚨Dijaga bahasanya bang jago",
"Jangan toxiclah bang jago🙏", "You kiss your mother with that mouth?🤡"]

if "responding" not in db.keys():
  db["responding"] = True


def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote=json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)


def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
      return

    msg = message.content
  
    if msg.startswith('-inspire'):
      quote = get_quote()
      await message.channel.send(quote)
    
    if db["responding"]:
      options = starter_encouragements
      gif = ["https://tenor.com/view/slap-in-the-face-angry-gtfo-bitc-bitch-slap-gif-15667197","https://tenor.com/view/slap-bear-slap-me-you-gif-17942299",
"https://tenor.com/view/slap-in-the-face-slap-hit-ouch-anger-gif-17283089"
,"https://tenor.com/view/slap-slapping-head-whack-gif-12667518"
,"https://tenor.com/view/batman-slap-robin-slap-gif-10206784"]

      if "encouragements" in db.keys():
        options = options + db["encouragements"]

      if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(options))
        await message.channel.send(random.choice(gif))


    if msg.startswith("-new"):
      encouraging_message = msg.split("-new ",1)[1]
      update_encouragements(encouraging_message)
      await message.channel.send("New encouraging message added! :v")

    if msg.startswith("-del"):
      encouragements = []
      if "encouragements" in db.keys():
        index = int(msg.split("-del",1)[1])
        delete_encouragement(index)
        encouragements = db["encouragements"]
      await message.channel.send(encouragements)

    if msg.startswith("-list"):
      encouragements = []
      if "encouragements" in db.keys():
        encouragements = db["encouragements"]
      await message.channel.send(encouragements)

    if msg.startswith("-responding"):
      value = msg.split("responding ",1)[1]

      if value.lower() == "true":
        db["responding"] = True
        await message.channel.send("Responding is on")
      else:
        db["responding"] = False
        await message.channel.send("Responding is off")


keep_alive()
client.run(os.getenv('TOKEN'))