import discord
from discord.ext import commands

bot_version = 2
command_prefix = '!'

startup_extensions = ["src.discord_channel_bot.channel"]
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
    await ctx.send(f'''Befehle:
    {command_prefix}help: Zeigt eine detaillierte Übersicht aller Befehle
    {command_prefix}hilfe: Zeigt eine Kurzübersicht aller Befehle
    
    {command_prefix}auf: Reaktiviert den aktuellen Kanal
    {command_prefix}hallo: Sagt hallo
    {command_prefix}neu <Kanalname>: Erzeugt neuen Kanal namens <Kanalname> in der gleichen Kategorie
    {command_prefix}version: Gibt die aktuelle Bot-Version aus
    {command_prefix}zu: Archiviert den aktuellen Kanal''')


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
