import os
import discord
from discord.ext import commands, tasks
from urllib import request

intents = discord.Intents(message_content=True, messages=True, reactions=True, guilds=True)
bot = commands.Bot(intents=intents, command_prefix='!')

token = os.environ['discord_token']
url = os.environ['server_url']
healthcheck = url + "/healthcheck"
channel = int(os.environ['audiobooks_channel'])
kymahi = int(os.environ['kymahi_id'])
audiobooks = int(os.environ['audiobooks_role'])

is_server_down = False


@tasks.loop(minutes=30.0)
async def server_up():
    global is_server_down

    try:
        status_code = request.urlopen("https://{}".format(healthcheck)).getcode()
        if status_code != 200:
            is_server_down = True
            print("it's down!")
            await send_msg("<@{}> The server is down!".format(kymahi))
        elif is_server_down:
            is_server_down = False
            await send_msg("<@&{}> Server is back online!".format(audiobooks))
            print("Server is back up. status_code: {}".format(status_code))
        else:
            print("Server is up. status_code: {}".format(status_code))
    except Exception as e:
        if not is_server_down:
            is_server_down = True
            print("it's down! {}".format(e))
            await send_msg("<@{0}> The server is down! {1}".format(kymahi, e))


@bot.event
async def on_ready():
    server_up.start()


@bot.command(name="ip")
async def ip(ctx):
    try:
        await ctx.send("https://{}".format(url))
    except Exception as e:
        await ctx.send("it broke: {}".format(e))
        await server_up()


@bot.command(name="address")
async def address(ctx):
    await ip(ctx)


async def send_msg(msg: str):
    await bot.get_channel(channel).send(msg)


bot.run(token)
