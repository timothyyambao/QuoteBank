import discord
import os
from replit import db
from keep_alive import keep_alive
import random

client = discord.Client()

#add function to add quotes to database
async def add(message):
    input = message.content.split("\n")
    input.remove(input[0])
    if len(input) != 3:
        await message.channel.send("""
    Please enter new line after every input (shift + enter), Example:
    $add
    "stuff"
    name 
    Date
    """)
        return

    if message.guild.id in db.keys():
        await message.channel.send("adding {} {} {}".format(
            input[0], input[1], input[2]))
        db[message.guild.id] += ([[input[0], input[1], input[2]]])
    else:
        await message.channel.send("adding {} {} {}".format(
            input[0], input[1], input[2]))
        db[message.guild.id] = [[input[0], input[1], input[2]]]


#delete function to delete quotes from database
async def delete(message):
    input = message.content[len('$del '):].split()

    try:
        numIndex = int(input[0]) - 1
        if numIndex > len(db[message.guild.id]):
            await message.channel.send(
                "can't delete something that's not there!")
            return
    except IndexError:
        await message.channel.send(
            "please send a delete request by listing the number you would like to delete from the list"
        )
        await print_quotes(message)
        await message.channel.send(
            "format your delete request by $del # \nfor example, '$del 4' would delete item #4"
        )
        return

    await message.channel.send("Deleting: {}".format(
        db[message.guild.id][numIndex]))
    valToDelete = db[message.guild.id][numIndex]
    testList = [x for x in db[message.guild.id] if x != valToDelete]
    del db[message.guild.id]
    db[message.guild.id] = testList

#shows a random quote entered
async def show(message):
    index = random.randint(0, len(db[message.guild.id]) - 1)
    i = db[message.guild.id][index]
    await message.channel.send('{}. {} -{}, {} \n'.format(
        str(index + 1), i[0], i[1], i[2]))


#prints list of all items in database
async def print_quotes(message):
    strToOutput = ''
    indexNum = 1

    #check if there is any content in server's database, if empty, prints no "quotes"
    if message.guild.id in db.keys():
        for i in db[message.guild.id]:
            strToOutput += '{}. {} -{}, {} \n'.format(str(indexNum), i[0], i[1], i[2])
            indexNum += 1
    else:
        await message.channel.send("QUOTE LIST EMPTY")
        return

    await message.channel.send(strToOutput)


#alerts console when connected, also sets activity to give information
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(
        name="type $help for list of commands"))

#checks message sent and runs certain function when called using $function
@client.event
async def on_message(message):
    #checks if message is sent by bot, if so, disregard by returning
    if message.author == client.user:
        return

    #help function that prints out commands
    if message.content.startswith('$help'):
        await message.channel.send("""
          Here are my commands:
          $help - help menu
          $add - add quote 
          $del - delete a quote
          $show - show a random quote
          $all - show ALL quotes
          """)

    if message.content.startswith('$add'):
        await add(message)

    if message.content.startswith('$del'):
        await delete(message)

    if message.content.startswith('$show'):
        await show(message)

    if message.content.startswith('$all'):
        await print_quotes(message)

    if message.content.startswith('$clearkeys'):
        await message.channel.send(
            'wiping all my quotes! say bye to all these!')
        await print_quotes(message)
        del db[message.guild.id]


keep_alive()
client.run(os.getenv('TOKEN'))
