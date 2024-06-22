#!/usr/bin/python
from typing import Optional
from dotenv import load_dotenv, dotenv_values
import discord
from discord import app_commands
import time
import datetime
import os
import string
import requests
import jq

load_dotenv()
token = os.getenv("TOKEN")
guild_id = os.getenv("GUILD_ID")
confessions_channel_id = os.getenv("CONFESSIONS_CHANNEL_ID")
logs_channel_id = os.getenv("LOGS_CHANNEL_ID")


MY_GUILD = discord.Object(id=guild_id)

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


@client.tree.command()
@app_commands.describe(
        confession='Your confession goes here',
)
async def confess(interaction: discord.Interaction, confession: str):
    """Posts a confession."""
    await interaction.response.send_message(f'Confession acknowledged!', ephemeral=True)
    
    confessions_channel = interaction.guild.get_channel(int(confessions_channel_id))
    logs_channel = interaction.guild.get_channel(int(logs_channel_id))
    embed = discord.Embed(title='Confession')
    log_embed = discord.Embed(title='Confession')
    embed.set_author(name='Anonymous')
    log_embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)
    embed.description = confession
    log_embed.timestamp = embed.timestamp = datetime.datetime.now()
    
    sent_confession = await confessions_channel.send(embed=embed)
    log_embed.description = f'{confession}\n\nhttps://discord.com/channels/{guild_id}/{confessions_channel_id}/{str(sent_confession.id)}'
    await logs_channel.send(embed=log_embed)


@client.tree.command()
async def cat(interaction: discord.Interaction):
    """Gives a cat."""
    get = requests.get("https://api.thecatapi.com/v1/images/search")
    print(f'Server response: {get.text}')
    url = jq.compile('.[] | .url').input_text(get.text).text()
    url = url.replace('"', '')
    cat = discord.Embed(title='Cat')
    cat.set_image(url=url)
    
    await interaction.response.send_message(embed=cat)


@client.tree.command()
async def dog(interaction: discord.Interaction):
    """Gives a dog."""
    get = requests.get("https://api.thedogapi.com/v1/images/search")
    print(f'Server response: {get.text}')
    url = jq.compile('.[] | .url').input_text(get.text).text()
    url = url.replace('"', '')
    dog = discord.Embed(title='Dog')
    dog.set_image(url=url)

    await interaction.response.send_message(embed=dog)


client.run(token)
