import discord
from discord.ext import commands


class Channel(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def is_admin(user):
        return True if Channel.find_named(user.roles, "Admins") else False

    @staticmethod
    def find_named(list_with_named, name):
        list_of_one = []
        if name in [item.name for item in list_with_named]:
            list_of_one = [item for item in list_with_named if item.name == name]

        return list_of_one[0] if len(list_of_one) == 1 else None

    @staticmethod
    async def get_category_or_clone(category_name, to_clone) -> discord.CategoryChannel:
        found_cat = Channel.find_named(to_clone.guild.categories, category_name)
        return found_cat or await to_clone.clone(name=category_name)

    @staticmethod
    async def move_channel(channel, new_category_name) -> discord.CategoryChannel:
        new_category = await Channel.get_category_or_clone(new_category_name, channel.category)
        await channel.edit(category=new_category)
        return new_category

    @commands.command(description='Erzeugt einen neuen Kanal namens <new_channel_name> in der gleichen Kategorie')
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

    async def __kopieren(self, ctx, anzahl: int, in_kanal: discord.TextChannel):
        if anzahl < 1 or not in_kanal or ctx.channel == in_kanal:
            return False

        messages = await ctx.channel.history(limit=anzahl + 1).flatten()
        messages = messages[1:len(messages)][::-1]  # remove first (latest) message and reverse list

        # TODO multimedialer Inhalt muss anders behandelt werden
        bulk = f'Kopiert/Verschoben von: {ctx.channel.mention}\n----------------------------------------------\n'
        for msg in messages:
            bulk += f'{msg.author.display_name}: {msg.content}\n'
        bulk += '----------------------------------------------'
        await in_kanal.send(bulk)
        return True

    @commands.command(description='Kopiert eine <anzahl> von Nachrichten in den Kanal namens <in_kanal_name>')
    async def kopieren(self, ctx, anzahl: int, in_kanal_name: str, send_message=True):
        if anzahl < 1:
            return

        channel = Channel.find_named(ctx.guild.text_channels, in_kanal_name)
        if await self.__kopieren(ctx, anzahl, channel) and send_message:
            await ctx.send(f'{anzahl} Nachrichten kopiert nach {channel.mention}')

    @commands.command(description='Entfernt eine <anzahl> von Nachrichten aus dem aktuellen Kanal')
    async def entfernen(self, ctx, anzahl: int, send_message=True):
        if not Channel.is_admin(ctx.author) or anzahl < 1:
            return

        messages = await ctx.channel.history(limit=anzahl + 1).flatten()
        messages = messages[::-1]  # reverse list
        await ctx.channel.delete_messages(messages)

        if send_message:
            await ctx.send(f'{anzahl} Nachrichten gelöscht')

    @commands.command(description='Verschiebt eine <anzahl> von Nachrichten in den Kanal namens <in_kanal_name>')
    async def verschieben(self, ctx, anzahl: int, in_kanal_name: str):
        if not Channel.is_admin(ctx.author) or anzahl < 1:
            return

        channel = Channel.find_named(ctx.guild.text_channels, in_kanal_name)
        if channel:
            if await self.__kopieren(ctx, anzahl, channel):
                await self.entfernen(ctx, anzahl, send_message=False)
                await ctx.send(f'{anzahl} Nachrichten verschoben nach {channel.mention}')


def setup(bot):
    bot.add_cog(Channel(bot))
