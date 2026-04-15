import discord
import os
from openai import OpenAI

client_openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # simple trigger
    if message.content.startswith("!ask"):
        user_input = message.content.replace("!ask", "").strip()

        response = client_openai.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": user_input}]
        )

        reply = response.choices[0].message.content

        await message.channel.send(reply)

client.run(os.getenv("DISCORD_TOKEN"))
