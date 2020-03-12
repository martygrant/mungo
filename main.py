##### Discord bot for Glasgow Developers, originally developed by Martin Grant
##### Created 08/10/2018
##### Last Update 08/10/2018
##### Version 0.1
##### Contributors
#
# https://github.com/medallyon
#
#####

import os
import random as rand
import sys
from datetime import datetime, timedelta
from time import time as timestamp
import asyncio
import discord
from discord.ext import commands
from discord.utils import get
import requests

import modules.roles
import modules.weather

REPOSITORY_URL = "https://github.com/martygrant/mungo"
VERSION_NUMBER = os.getenv('version')
BOT_TOKEN = os.getenv('token')

##### [ BOT INSTANTIATION ] #####

BOT = commands.Bot(description="Below is a listing for Mungo's commands. Use '!' infront of any of them to execute a command, like '!help'", command_prefix="!")
BOT.load_extension('modules.roles')
#BOT.load_extension('modules.weather')

##### [ EVENT LISTENERS ] #####

@BOT.event
async def on_ready():
	"""The 'on_ready' event"""
	print("Logged in as {} ({})\n------".format(BOT.user.name, BOT.user.id))

@BOT.event
async def on_member_join(member):
	"""The 'on_member_join' event"""
	
	generalChannel = BOT.get_channel('497797810834636808')
	introductionsChannel = BOT.get_channel('498797757620813834')
	welcomeRulesChannel = BOT.get_channel('498797001043869697')
	eventsChannel = BOT.get_channel('498796966365495298')
	junkChannel = BOT.get_channel('498856942060699669')

	welcome_message = """Welcome to the **Glasgow Game Developers** server!

Please check out {}. Visit {} to see what events are coming up! Why not introduce yourself in {}?

Type `!help` for a list of my commands.

Use `!role <role name>` to add a role to your account. Use `!roles` to see what roles are available. This must be done in the {} channel.

""".format("{}".format(welcomeRulesChannel.mention), "{}".format(eventsChannel.mention), "{}".format(introductionsChannel.mention), "{}".format(junkChannel.mention))

	# Send the welcome message to the user individually
	await BOT.send_message(member, welcome_message)
	# Announce a new member joining in the general channel
	await BOT.send_message(generalChannel, "Welcome {} to the Glasgow Game Developers server!".format(member.mention))

@BOT.event
async def on_member_remove(member):
	"""The 'on_member_remove' event"""

	junkChannel = BOT.get_channel('498856942060699669')

	await BOT.send_message(junkChannel, "User **{}** has left the server. Goodbye!".format(str(member)))


##### [ BOT COMMANDS ] #####

@BOT.command()
async def say(*something):
	"""Make Mungo say something."""
	if something:
		await BOT.say(" ".join(something))

@BOT.command()
async def about():
	"""Information about the Mungo bot."""

	info = "I'm Mungo, the bot for the Glasgow Game Developers discord server.\nNamed after St. Mungo, the founder and patron saint of Glasgow.\nMy avatar is a street art mural by Smug on High Street.\n"
	info += "This is v"
	info += VERSION_NUMBER
	info += ". You can view and contribute to the bot, check out: "
	info += REPOSITORY_URL

	await BOT.say(info)
	
	
def getOnlineUserCount(users):
	count = 0
	for user in users:
		if str(user.status) == "online" or str(user.status) == "idle" or str(user.status) == "dnd":
			count += 1
	return count


def getNewestMember(users):
	userList = list(users)

	newest = userList[0]
	for x in userList[2:]:
		if x.joined_at > newest.joined_at:
			newest = x

	return newest


@BOT.command()
async def stats(ctx):
	"""Get server statistics."""
	server = ctx.message.author.guild
	serverName = server.name
	numberOfUsers = server.member_count
	members = server.members
	numberOfOnlineUsers = getOnlineUserCount(members)
	createdDate = server.created_at.strftime('%Y-%m-%d')
	newestMember = getNewestMember(members)

	embed = discord.Embed(type="rich", colour=utils.generate_random_colour(), timestamp=datetime.now())
	embed.set_thumbnail(url=server.icon_url)
	embed.set_author(name=serverName)
	embed.add_field(name="Created", value=createdDate)
	embed.add_field(name="Users Online", value=numberOfOnlineUsers)
	embed.add_field(name="Users Total", value=numberOfUsers)
	embed.add_field(name="Newest Member", value=newestMember)

	await ctx.message.channel.send(embed=embed)

##### [ BOT LOGIN ] #####

BOT.run(BOT_TOKEN)
