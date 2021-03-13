import discord
import os
from replit import db

client = discord.Client()

#for add function 
async def update_callbacks(message, msgArray):
  if message.guild.id in db.keys():
    await message.channel.send("addings {} {} {}".format(msgArray[0],msgArray[1],msgArray[2]))
    db[message.guild.id]+=([[msgArray[0],msgArray[1],msgArray[2]]])
  else:
    await message.channel.send("adding {} {} {}".format(msgArray[0],msgArray[1],msgArray[2]))
    db[message.guild.id] = [[msgArray[0],msgArray[1],msgArray[2]]]


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$help'):
        await message.channel.send(
          """
          Here are my commands:
          $help - help menu
          $add - add callback 
          $show - show a random callback
          $all - show ALL callbacks
          """
      )
    
    if message.content.startswith('$showserver'):
      await message.channel.send(message.guild.id)
    
    if message.content.startswith('$add'):
      input = message.content[len('$add '):].split("\n") 
      if len(input) != 3: 
        await message.channel.send("""
        Please enter new line after every input (shift + enter), Example:
        $add
        "stuff"
        name 
        Date
        """)
        return
      await update_callbacks(message,input)
    
    if message.content.startswith('$show'):
      await message.channel.send(db[message.guild.id])

    if message.content.startswith('$clearkeys'):
      await message.channel.send('wiping all my callbacks! say bye to all these!')
      await message.channel.send(db[message.guild.id])
      del db[message.guild.id]

client.run(os.getenv('TOKEN')) 
