import discord
from discord.ext import commands
from functions import *
import pymongo
from pymongo import DESCENDING, MongoClient

adminList = []
adminList.append(00000) #my discord id, removed
adminList.append(00000) #another discord id, also removed from the code

cluster = MongoClient(
    "mongodb+srv://egws:V7HXBVSYMC8Qe0SK@stestes.pal4o.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
)
db = cluster["DB"]
collection = db["Users"]

class admin(commands.Cog):

    def __init__(self,client):
        self.client = client

    @commands.command(aliases=['give'])
    async def give_points(self,ctx,points:float,*,user):
        if await isAdmin(ctx.author):
            v = collection.find_one({"display_name": str(user)})
            if v == None:
                await ctx.send('User {} not found.\nPlease make use you typed the correct username or use the update command and try again'.format(user))
            else:
                collection.update_one({"display_name": str(user)},{"$inc": {"points": points }})
                await ctx.send("{} points given to {}".format(points,user))
        else:
            await ctx.send("You are not authorized to use this command")
    
    @commands.command(aliases=['take'])
    async def take_points(self,ctx,points:float,*,user):
        points = points * -1
        if await isAdmin(ctx.author):
            v = collection.find_one({"display_name": str(user)})
            if v == None:
                await ctx.send('User {} not found.\nPlease make use you typed the correct username or use the update command and try again'.format(user))
            else:
                collection.update_one({"display_name": str(user)},{"$inc": {"points": points }})
                await ctx.send("{} points removed from {}".format(points,user))
        else:
            await ctx.send("You are not authorized to use this command")

    @commands.command(aliases=['set'])
    async def set_points(self,ctx,points:float,*,user):
        if await isAdmin(ctx.author):
            v = collection.find_one({"display_name": str(user)})
            if v == None:
                await ctx.send('User {} not found.\nPlease make use you typed the correct username or use the update command and try again'.format(user))
            else:
                collection.update_one({"display_name": str(user)},{"$set": {"points": points }})
                await ctx.send("{} points set for {}".format(points,user))
        else:
            await ctx.send("You are not authorized to use this command")
    
    @commands.command(aliases=['running'])
    async def running_since(self,ctx):
        if await isAdmin(ctx.author):
            await ctx.send('Bot has been running since ' + str(self.client.now))
        else:
            await ctx.send("You are not authorized to use this command")

    @commands.command(aliases=['off'])
    async def shutdown(self,ctx):
        if await isAdmin(ctx.author):
            await self.client.close()
        else:
            await ctx.send("You are not authorized to use this command")

    





def setup(client):
    client.add_cog(admin(client))