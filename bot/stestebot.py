import collections
import discord
from discord import user
from discord import guild
from discord.ext import tasks
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands.core import command
import time
import datetime
import pymongo
from pymongo import DESCENDING, MongoClient
import os
from functions import *
#from keep_alive import keep_alive

cluster = MongoClient(
    "mongodb server link, password and stuff, removed from the code for obvious reasons"
)
db = cluster["DB"]
collection = db["Users"]

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='!', intents=discord.Intents.all())
now = datetime.datetime.now()
now = now.strftime("%d/%m/%Y %H:%M:%S")
client.now = now
print("Started running at: ", now)

adminList = []
adminList.append(00000) #my discord id, removed
adminList.append(00000) #another discord id, also removed from the code
client.adminList = adminList

client.log = []
client.log.append("Started running at: " + now)

print("lmao")

trololo = 0

print(datetime.datetime.now().strftime("%H"))

#Events
@client.event
async def on_ready():
    print('Bot is ready.')
    pointspoints.start()
    updateupdate.start()
    dailydaily.start()

@client.event
async def on_voice_state_update(member, before, after):
    if await userJoined(member, before, after):
        await createUser(member)


#Tasks
@tasks.loop(minutes=15)
async def dailydaily():
    tora = datetime.datetime.now().strftime("%H")
    if (tora == "23"):
        users = collection.find({})
        print("setting daily 1 for everyone")
        for u in users:
            collection.update_one({"_id": u["_id"]},{"$set": {"daily": 1}})

        print("succesfully set daily 1 for everyone")

@tasks.loop(seconds=6)
async def pointspoints():
    serv = client.get_guild(11111) #id removed from the code
    people = 0
    bonus = 0.00
    tora = datetime.datetime.now().strftime("%H")
    chans = serv.channels
    for c in chans:
        people = 0
        if str(c.type) == "voice" and c.id != 11111:  #id removed from the code

            for member in c.members:

                #Determine amount of people in each channel
                if not await userMuted(member) and not await userDeaf(member):
                    people+=1

            bonus = (people-1)/100

            if people < 4:
                bonus = (people-1)*0.02

            if people >= 4:
                bonus = 0.04 + (people-3)*0.01

            if (people == 1):
                bonus = -0.05
            
            

            for member in c.members:
                #Daily Bonus
                if collection.find_one({"_id": int(member.id)})["daily"] == 1 and tora != "23":
                    print("daily bonus to " + str(member.display_name))
                    collection.update_one({"_id": int(member.id)},{"$inc": {"points": 30}})
                    collection.update_one({"_id": int(member.id)},{"$set": {"daily": 0}})

                #Awarding points to each member in VC
                if await userDeaf(member):
                    collection.update_one({"_id": int(member.id)},{"$inc": {"points": 0.01 }})
                elif await userMuted(member):
                    collection.update_one({"_id": int(member.id)},{"$inc": {"points": 0.04 }})
                elif not await userMuted(member) and not await userDeaf(member):
                    collection.update_one({"_id": int(member.id)},{"$inc": {"points": 0.1+bonus}})

                #Rounding points because python doesn't like decimals
                v = collection.find_one({"_id": int(member.id)})
                pp = v["points"]
                collection.update_one({"_id": int(member.id)},{"$set": {"points": round(pp,2) }})
                await update_last_online(member)


@tasks.loop(hours=1)
async def updateupdate():
    print ("Attempting to update users...")
    global g
    g = client.get_guild(11111) #id removed from the code
    users = collection.find({})
    for u in users:
        await update_user(u["_id"])
    print ("Users Updated according to schedule")


#Commands
@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

@client.command()
async def reload(ctx, extension=None):
    if extension != None:
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
        await ctx.send("Reloaded " + str(extension))
    else:
        await ctx.send("Reloading all cogs")
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    client.unload_extension(f'cogs.{filename[:-3]}')
                    client.load_extension(f'cogs.{filename[:-3]}')
                except:
                    print("exception occured while reloading cogs, its probably nothing tho")
        await ctx.send("Reloaded all cogs")



@client.command()
async def hello(ctx):
    await ctx.send('Hello Friend')

@client.command()
async def create(ctx, member: discord.User):
    if await isAdmin(ctx.author):
        await createUser(member)
        await ctx.send('User Created')
    else:
        await ctx.send("You are not authorized to use this command my friend")



@client.command()
async def remove(ctx, * , member):
    if await isAdmin(ctx.author):
        result = collection.delete_one({'display_name': member})
        await ctx.send("User removed")
    else:
        await ctx.send("You are not authorized to use this command my friend")


@client.command()
async def show(ctx, * , member=None):
    if member is None:
        member = ctx.author.display_name
    v = collection.find_one({"display_name": str(member)})
    #ping = '<@' + str(v["_id"]) + '>'
    if v == None:
        await ctx.send(
            'User {} not found.\nPlease make use you typed the correct username or use the update command and try again'
            .format(member))
    else:
        await ctx.send(
            'Displaying data for user: {}\n{} points\nlast seen on voice: {} (GMT)'.
            format(member, v["points"], v["last_online"]))


@client.command()
async def points(ctx, * , member=None):
    if member is None:
        member = ctx.author.display_name
    v = collection.find_one({"display_name": str(member)})
    if v == None:
        await ctx.send(
            'User {} not found.\nPlease make use you typed the correct username or use the update command and try again'
            .format(member))
    else:
        await ctx.send('{} has {} points'.format(member, v["points"]))


@client.command(aliases=['vibecheck','lb'])
async def leaderboard(ctx,num=1):
    await ctx.send('Here is the leaderboard: ')

    channel = ctx.message.channel
    embed = discord.Embed(title=':trophy: Leaderboard :trophy:',
                    colour=discord.Colour.green())

    
    i=0
    j=25*(num-1)

    users = collection.find({}).sort("points", pymongo.DESCENDING)

    for u in users:
        try:
            i += 1
            if (i>j): 
                embed.add_field(name=str(i) + '. ' + u["display_name"],
                            value=str(u["points"]),
                            inline=True)
        except:
            print("Error on leaderboard for user: ", str(u["_id"]))

    await ctx.channel.send(embed=embed)


@client.command()
async def update(ctx):
    global g
    guildID = ctx.message.guild.id
    g = client.get_guild(guildID)
    users = collection.find({})
    for u in users:
        await update_user(u["_id"])

    await ctx.send("Users updated succesfully... i think")


#Funtions, some are here, some are in functions.py

#User Management related Functions

async def createUser(member):
    if not await user_exists(member.id):
        print("{} does NOT exist, hence it has been created".format(member.id))

        post = {
            "_id": member.id,
            "display_name": member.display_name,
            "points": 0.0,
            "last_online":datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "daily":0
        }
        collection.insert_one(post)


async def user_exists(id):
    if collection.count_documents({"_id": int(id)}, limit=1):
        return True
    else:
        return False


async def update_user(id):
    try:
        global g
        member = g.get_member(id)
        collection.update_one({"_id": int(id)},{"$set": {"display_name": member.display_name}})
    except Exception as e:
        print("Couldn't find member in this server or an error occured",
              collection.find_one({"_id": int(id)})["display_name"])
        print(e)


async def update_last_online(member):
    d = datetime.datetime.now()
    collection.update_one({"_id": int(member.id)}, {
        "$set": {
            "last_online":
            d.strftime("%d/%m/%Y %H:%M:%S")
        }
    })

#Voice State Functions --> moved to functions.py


async def addToLog(thingy:str):
    d = datetime.datetime.now()
    d = d.replace(hour = d.hour+3)
    d = d.strftime("%d/%m/%Y %H:%M:%S")
    client.log.append(d + ": " + thingy)

client.remove_command("help")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

#keep_alive()
client.run('discord bot token, removed from obvious reasons')