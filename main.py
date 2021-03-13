import discord
import os
from replit import db

client = discord.Client()



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
      await message.channel.send(input)

client.run(os.getenv('TOKEN')) 
