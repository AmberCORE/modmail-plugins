import re

import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel

class Role(commands.Cog):
    """easily create roles and add them to your members."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def role(self, ctx, member: discord.Member, role: discord.Role):
        """assign a role to a member."""
        if role.position > ctx.author.roles[-1].position:
            return await ctx.send("You do not have permissions to give this role")
        await member.add_roles(role)
        await ctx.send("Successfully added the role to the user!")

    @commands.command()
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def unrole(self, ctx, member: discord.Member, role: discord.Role):
        """remove a role from a member."""
        if role.position > ctx.author.roles[-1].position:
            return await ctx.send("You do not have permissions to remove this role")
        await member.remove_roles(role)
        await ctx.send("Successfully removed the role from the user!")

    @commands.command(aliases=["makerole"])
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def createrole(self, ctx, name, color: str):
        """create a role."""
        valid = re.search(r"^#(?:[0-9a-fA-F]{3}){1,2}$", color)
        if not valid:
            embed = discord.Embed(title="Failure", color=self.bot.main_color,
                description="Please enter a **valid** [hex code](https://htmlcolorcodes.com/color-picker)")
            return await ctx.send(embed=embed)

        await ctx.guild.create_role(name=name, color=int(color.replace("#", "0x"), 0))
        await ctx.send("Successfully created the role!")
        
    @createrole.error
    async def createrole_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="No tag provided!", description="Please provide your player tag.", color=0xFF0000)
            return await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Role(bot))
    
