# Required library imports
import discord  # Main library for creating Discord bot
from mcstatus import JavaServer  # Allows checking Minecraft server status
import requests  # For HTTP requests
from mcrcon import MCRcon  # For Minecraft server RCON connection
import os  # For operating system operations
import time  # For time-related functions
from watchdog.observers import Observer  # For watching file changes
from watchdog.events import FileSystemEventHandler  # For handling filesystem events
import re  # Library for regular expressions
import subprocess  # For process handling
import asyncio  # Library for asynchronous coroutines

# List of authorized user IDs (operators)
AUTHORIZED_USERS = [
    123456789,  # Replace with Discord operator IDs
]

# Path to the server start batch file
SERVER_START_SCRIPT = r"D:\Server\Run\File.bat"  # Replace the .bat file path

# Bot permissions configuration
intents = discord.Intents.default()
intents.message_content = True  # Allows the bot to read messages

# Discord client initialization
client = discord.Client(intents=intents)

# Event triggered when the bot is ready
@client.event
async def on_ready():
    print(f'Bot connected as {client.user}')
    # Start the log file observer
    observer = setup_log_watcher(client)

# Discord channel ID where messages will be sent
DISCORD_CHANNEL_ID = "123456789"  # Replace with your channel ID

# Event triggered when a message is received
@client.event
async def on_message(msg):
    # Only respond to messages in the specified channel
    if msg.channel.id != int(DISCORD_CHANNEL_ID):
        return

    if msg.author == client.user:
        return

    # Handle $start command
    if msg.content.startswith('$start'):
        if msg.author.id in AUTHORIZED_USERS:
            try:
                # Change to the server directory first
                server_directory = os.path.dirname(SERVER_START_SCRIPT)
                os.chdir(server_directory)
                
                # Execute the batch file in a new terminal window
                cmd = f'start cmd /k "{SERVER_START_SCRIPT}"'
                subprocess.Popen(cmd, shell=True)
                
                await msg.channel.send("Starting Minecraft server! ⚡")
            except Exception as e:
                await msg.channel.send(f"Error starting server: {str(e)} ❌")
        else:
            await msg.channel.send("You don't have permission to use this command 🚫")

    # Command $server - Checks Minecraft server status
    if msg.content.startswith('$server'):
        try:
            public_ip = requests.get('https://api.ipify.org')
            if public_ip:
                # Try to connect to the Minecraft server
                server = JavaServer.lookup(f"{public_ip}:25565")
                status = server.status()
                # Send information about connected players
                await msg.channel.send(f"Server is online! 🟢\nPlayers online: {status.players.online}/{status.players.max}")
            else:
                await msg.channel.send("Couldn't get server IP address! ⚠️")
        except:
            await msg.channel.send("Server is offline or unavailable! 🔴")

# Start the bot with authentication token
client.run("YOUR_TOKEN")