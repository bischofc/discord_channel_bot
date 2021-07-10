import discord
from discord.ext import commands

from .utils import is_admin, is_beta_tester, find_named


class Message(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def __kopieren(ctx, anzahl: int, in_kanal: discord.TextChannel):
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

    @commands.command(description='Kopiert eine <anzahl> von Nachrichten in den Kanal namens <in_kanal_name> '
                                  '(nur für Admins und Beta-Tester)')
    async def kopieren(self, ctx, anzahl: int, in_kanal_name: str):
        if anzahl < 1 or not is_beta_tester(ctx.author):  # TODO: Beta-Tester
            return

        channel = find_named(ctx.guild.text_channels, in_kanal_name)
        if await Message.__kopieren(ctx, anzahl, channel):
            await ctx.send(f'{anzahl} Nachrichten kopiert nach {channel.mention}')

    @commands.command(description='Entfernt eine <anzahl> von Nachrichten aus dem aktuellen Kanal (nur für Admins)')
    async def entfernen(self, ctx, anzahl: int, send_message=True):
        if not is_admin(ctx.author) or anzahl < 1:
            return

        messages = await ctx.channel.history(limit=anzahl + 1).flatten()
        messages = messages[::-1]  # reverse list
        await ctx.channel.delete_messages(messages)

        if send_message:
            await ctx.send(f'{anzahl} Nachrichten gelöscht')

    @commands.command(description='Verschiebt eine <anzahl> von Nachrichten in den Kanal namens <in_kanal_name> '
                                  '(nur für Admins und Beta-Tester)')
    async def verschieben(self, ctx, anzahl: int, in_kanal_name: str):
        if not is_admin(ctx.author) or \
                not is_beta_tester(ctx.author) or \
                anzahl < 1:  # TODO: Beta-Tester
            return

        channel = find_named(ctx.guild.text_channels, in_kanal_name)
        if channel:
            if await Message.__kopieren(ctx, anzahl, channel):
                await self.entfernen(ctx, anzahl, send_message=False)
                await ctx.send(f'{anzahl} Nachrichten verschoben nach {channel.mention}')


def setup(bot):
    bot.add_cog(Message(bot))
