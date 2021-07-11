import discord
from discord.ext import commands

from .utils import is_admin

bot_version = 4
command_prefix = '!'

startup_extensions = ["src.discord_channel_bot.channel", "src.discord_channel_bot.message"]
bot_description = '''Bot, der beim Kanalmanagement hilft.
Er kann z.B. neue Kanäle eröffnen, archivieren und wieder aktivieren.'''

# Set intents and create client
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=command_prefix, description=bot_description, intents=intents)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.event
async def on_error(event, *args, **kwargs):
    if event == 'on_message':
        await args[0].channel.send(
            "Das hat nicht funktioniert, bitte versuch es nochmal... aber anders. Oder wende Dich an einen Admin.")


@bot.event
async def on_member_join(member):
    await member.send(
        "Herzlich willkommen zur Institutstr!\nTippe '!hilfe' in einen Kanal, um zu sehen, was Du tun kannst.")


@bot.command(description='Zeigt eine Kurzübersicht aller Befehle')
async def hilfe(ctx):
    prefix = command_prefix
    msg = f'''Befehle:
    {prefix}help: Zeigt eine detaillierte Übersicht aller Befehle
    {prefix}hilfe: Zeigt eine Kurzübersicht aller Befehle
    
    {prefix}auf: Reaktiviert den aktuellen Kanal
    {prefix}hallo: Sagt hallo
    {prefix}neu <Kanalname>: Erzeugt neuen Kanal namens <Kanalname> in der gleichen Kategorie
    {prefix}version: Gibt die aktuelle Bot-Version aus
    {prefix}zu: Archiviert den aktuellen Kanal'''

    if is_admin(ctx.author):
        msg += f'''\n\nAdmin-Befehle:
    {prefix}entfernen <anzahl>: Entfernt die letzten <anzahl> Einträge
    {prefix}kopieren <anzahl> <in_kanal_name>: Kopiert die letzten <anzahl> Einträge in <in_kanal_name> \
    (nur Beta-Tester)
    {prefix}verschieben <anzahl> <in_kanal_name>: Verschiebt die letzten <anzahl> Einträge in <in_kanal_name> \
    (nur Beta-Tester)'''

    await ctx.send(msg)


@bot.command(description='Sagt hallo')
async def hallo(ctx):
    await ctx.send(f'Hallo {ctx.author.display_name}!')


@bot.command(description='Gibt die aktuelle Bot-Version aus')
async def version(ctx):
    await ctx.send(f'Version: {bot_version}')


def run(token):
    # Load extensions
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run(token)
