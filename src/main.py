#!/usr/bin/python
from typing import Optional
from dotenv import load_dotenv, dotenv_values
import discord
from discord import app_commands
import time
import datetime
import os
import string

load_dotenv()

MY_GUILD = discord.Object(id=f'{os.getenv("GUILD_ID")}')

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

#Post, not as reply
#await log_channel.send('Hewwo! uwu')

#Post as reply, only seen by sender
#await interaction.response.send_message(f'Confession acknowledged!', ephemeral=True)



@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')

@client.event
async def on_message(message):
    print(f'[{time.ctime()}] Message from {message.author}: {message.content}')


@client.tree.command()
@app_commands.describe(
        confession='Your confession goes here',
)
async def confess(interaction: discord.Interaction, confession: str):
    """Posts a confession."""
    await interaction.response.send_message(f'Confession acknowledged!', ephemeral=True)
    
    confessions_channel = interaction.guild.get_channel(int(f'{os.getenv("CONFESSIONS_CHANNEL_ID")}'))
    logs_channel = interaction.guild.get_channel(int(f'{os.getenv("LOGS_CHANNEL_ID")}'))
    embed = discord.Embed(title='Confession')
    log_embed = discord.Embed(title='Confession')
    embed = embed.set_author(name='Anonymous')
    log_embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)
    log_embed.description = embed.description = confession
    log_embed.timestamp = embed.timestamp = datetime.datetime.now()
    
    await confessions_channel.send(embed=embed)
    await logs_channel.send(embed=log_embed)


client.run(f'{os.getenv("TOKEN")}')
