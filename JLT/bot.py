import discord
from discord.ext import tasks
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os
import django
from datetime import datetime

# Load Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'JLT.settings')
django.setup()

from listings.models import Livraison  # Import your Django models if needed

TOKEN = "MTM1MzgzNDk4MTg4NTIxODk3OA.GUEOC4.YeL9EGnuLyzvGXI1E5BVN4h5cfeJf4JapVWUyw"
CHANNEL_ID = 1175212358474420234  # Replace with your channel ID

intents = discord.Intents.default()
client = discord.Client(intents=intents)
scheduler = AsyncIOScheduler()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    scheduler.add_job(send_reminder, 'cron', hour=6, minute=0)  # 08:00 AM
    scheduler.add_job(send_reminder, 'cron', hour=10, minute=0)  # 12:00 PM
    scheduler.add_job(send_reminder, 'cron', hour=13, minute=0)  # 16:00 PM
    scheduler.start()

async def send_reminder():
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("@livreur N'oubliez pas de vérifier l'étagère à craquelin/pains/desserts ! ")

client.run(TOKEN)
