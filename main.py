import discord
import os
import sys

if __name__ == '__main__':

    # Set bot prefix
    prefix = '!'

    # Get bot login token
    if len(sys.argv) == 2:
        token = sys.argv[1]
    else:
        token = os.getenv("DC_BOT_TOKEN")
    if not token:
      sys.exit("No token found: Please pass as argument or as environment variable named DC_BOT_TOKEN")

    # Set intents and create client
    intents = discord.Intents.default()
    intents.members = True
    client = discord.Client(intents=intents)


    async def clone_category_if_not_exists(category, new_category_name):
        existing_category_names = list(map(lambda c: c.name, category.guild.categories))

        if new_category_name in existing_category_names:
            cat_list_of_one = [cat for cat in category.guild.categories if cat.name == new_category_name]
            return cat_list_of_one[0]

        return await category.clone(name=new_category_name)


    @client.event
    async def on_error(event, *args, **kwargs):
        if event == 'on_message':
            await args[0].channel.send(
                "Das hat nicht funktioniert, bitte versuch es nochmal... aber anders. Oder wende Dich an einen Admin.")


    @client.event
    async def on_member_join(member):
      await member.send("Herzlich willkommen zur Institutstr!\nTippe '!hilfe' in einen Kanal, um zu sehen, was Du tun kannst.")


    @client.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(client))


    @client.event
    async def on_message(message):
        if message.author == client.user or not message.content.startswith(prefix):
            return

        if message.content.startswith(f'{prefix}hilfe') or message.content.startswith(f'{prefix}help'):
            await message.channel.send('''Befehle:
                !hilfe / !help: Zeigt alle Befehle
                !hallo: Sagt hallo
                !neu <Kanalname>: Erzeugt neuen Kanal namens <Kanalname> in der gleichen Kategorie
                !zu: Archiviert den aktuellen Kanal
                !auf: Reaktiviert den aktuellen Kanal''')

        if message.content.startswith(f'{prefix}hallo'):
            await message.channel.send(f'Hallo {message.author.display_name}!')

        if message.content.startswith(f'{prefix}neu '):
            new_channel_name = message.content.replace(f"{prefix}neu ", "")
            new_channel = await message.guild.create_text_channel(new_channel_name, category=message.channel.category)
            await message.channel.send(
                f'Kanal {new_channel.mention} wurde in Kategorie "{new_channel.category}" erstellt.')

        if message.content.startswith(f'{prefix}zu'):
            if message.channel.category.name.endswith("-Archiv"):
                return

            archive_category_name = message.channel.category.name + '-Archiv'
            archive_category = await clone_category_if_not_exists(message.channel.category, archive_category_name)
            await message.channel.edit(category=archive_category)
            await message.channel.send(f"Archiviert in Kategorie {archive_category.mention}")

        if message.content.startswith(f'{prefix}auf'):
            if not message.channel.category.name.endswith("-Archiv"):
                return

            open_category_name = message.channel.category.name.replace("-Archiv", "")
            open_category = await clone_category_if_not_exists(message.channel.category, open_category_name)
            await message.channel.edit(category=open_category)
            await message.channel.send(f"Reaktiviert in Kategorie {open_category.mention}")

    client.run(token)
