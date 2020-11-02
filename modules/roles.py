import discord
from discord.ext import commands
import utilities as utils


class Roles(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.restrictedRoles = ['Bot', 'Moderator', '@everyone']

	@commands.command(pass_context=True)
	async def roles(self, ctx):
		"""Print a list of all server roles."""
		roleString = ""
		count = 0

		rolesDict = {}

		for role in ctx.message.author.guild.roles:
			if role.name not in self.restrictedRoles:
				rolesDict[role.name] = 0
		
		# For each server role, for each user's list of roles, add to a count if there is a user with that role
		for role in ctx.message.author.guild.roles:
			if role.name not in self.restrictedRoles:
				for user in ctx.message.author.guild.members:
					for userRole in user.roles:
						if role == userRole:
							rolesDict[role.name] += 1

		# Convert dict to list so we can sort alphabetically
		rolesList = []
		for k, v in rolesDict.items():
			rolesString = "`"
			rolesString += k
			rolesString += "` "
			rolesString += str(v)
			rolesString += "\n"
			rolesList.append(rolesString)

		rolesList = sorted(rolesList)

		# Convert list to string so we can display using line terminator \n
		rolesString = ""
		for x in rolesList:
			rolesString += x

		embed = discord.Embed(type="rich", colour=utils.generate_random_colour())
		embed.set_author(name="Use '!role Role Name' to add a role to your profile.")
		embed.add_field(name="Roles", value=rolesString)

		await ctx.send(embed=embed)


	@commands.command(pass_context=True)
	async def role(self, ctx, *arg):
		"""Add or remove a role, e.g "!role Hobbyist" to add or remove the role "Hobbyist"."""
		user = ctx.message.author
		roleToAdd = ""
		for x in arg:
			roleToAdd += str(x)
			roleToAdd += " "
		roleToAdd = roleToAdd[:-1]

		if roleToAdd not in self.restrictedRoles:
			role = None

			# compare role argument with server roles by checking their lower-case representations
			for tempRole in ctx.message.author.guild.roles:
				if tempRole.name.lower() == roleToAdd.lower():
					print("MATCH! " + tempRole.name + " " + roleToAdd)
					role = tempRole
					break

			if role is None:
				return await ctx.send("That role doesn't exist.")

			# we want to skip removing the specified role if we are adding one
			dontRemove = False

			if role not in user.roles:
				await user.add_roles(role)
				await ctx.send("{} role has been added to {}.".format(role, user.mention))
				dontRemove = True

			if role in user.roles and dontRemove == False:
				await user.remove_roles(role)
				await ctx.send("{} role has been removed from {}.".format(role, user.mention))

		else:
			await ctx.send("This role requires manual approval from an admin.")

def setup(bot):
	bot.add_cog(Roles(bot))
	print("Roles module loaded.")
