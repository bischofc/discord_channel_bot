import discord
from discord.ext import commands


class Channel(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def get_category_or_clone(category_name, to_clone) -> discord.CategoryChannel:
        existing_categories = to_clone.guild.categories
        existing_category_names = list(map(lambda c: c.name, existing_categories))

        if category_name in existing_category_names:
            cat_list_of_one = [cat for cat in existing_categories if cat.name == category_name]
            return cat_list_of_one[0]

        else:
            return await to_clone.clone(name=category_name)

    @staticmethod
    async def move_channel(channel, new_category_name) -> discord.CategoryChannel:
        new_category = await Channel.get_category_or_clone(new_category_name, channel.category)
        await channel.edit(category=new_category)
        return new_category

    @commands.command(description='Erzeugt einen neuen Kanal namens "new_channel_name" in der gleichen Kategorie')
    async def neu(self, ctx, new_channel_name: str):
        new_channel = await ctx.guild.create_text_channel(new_channel_name, category=ctx.channel.category)
        await ctx.send(
            f'Kanal {new_channel.mention} wurde in Kategorie "{new_channel.category}" erstellt.')

    @commands.command(description='Archiviert den aktuellen Kanal')
    async def zu(self, ctx):
        if ctx.channel.category.name.endswith("-Archiv"):
            return

        category = await Channel.move_channel(ctx.channel, ctx.channel.category.name + '-Archiv')
        await ctx.send(f"Archiviert in Kategorie {category.mention}")

    @commands.command(description='Reaktiviert den aktuellen Kanal')
    async def auf(self, ctx):
        if not ctx.channel.category.name.endswith("-Archiv"):
            return

        category = await Channel.move_channel(ctx.channel, ctx.channel.category.name.replace("-Archiv", ""))
        await ctx.send(f"Reaktiviert in Kategorie {category.mention}")


def setup(bot):
    bot.add_cog(Channel(bot))
