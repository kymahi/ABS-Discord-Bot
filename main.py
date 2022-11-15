import discord
from discord.ext import commands, tasks
import socket
from urllib import request
from urllib.parse import urlsplit, urlparse
import threading
from http.client import HTTPConnection

intents = discord.Intents(message_content=True, messages=True, reactions=True, guilds=True)
bot = commands.Bot(intents=intents, command_prefix='!')

ipf = "ip.txt"

f = open("token.txt", "r")
token = f.read()
f.close()

url = ""
channel = -1
kymahi = -1
audiobooks = -1

is_server_down = False


@tasks.loop(minutes=30.0)
async def server_up():
    global is_server_down

    connection = HTTPConnection(host=url, timeout=10)
    try:
        connection.connect()
        if is_server_down:
            is_server_down = False
            await send_msg("{} Server is back online!".format(audiobooks))
        print("Server is up")
    except Exception as e:
        if not is_server_down:
            is_server_down = True
            print("it's down! {}".format(e))
            await send_msg("{0} The server is down! {1}".format(kymahi, e))
    finally:
        connection.close()


@tasks.loop(hours=12.0)
async def ip_changed():
    f = open(ipf, "r")
    text = f.read()
    f.close()
    new_ip = get_ip()
    if text:
        if text == new_ip:
            print("No IP change")
        else:
            print("IP is now {}".format(new_ip))
            f = open(ipf, "w")
            f.write(new_ip)
            await send_msg("{0} The IP address has changed to {1}".format(audiobooks, new_ip))
            f.close()
    else:
        print("No IP set. Set to {}".format(new_ip))
        f = open(ipf, "w")
        f.write(new_ip)
        f.close()


@bot.event
async def on_ready():
    open(ipf, "a+").close()
    
    server_up.start()
    ip_changed.start()

    global url
    global channel
    global kymahi
    global audiobooks

    f = open("url.txt", "r")
    url = f.read().splitlines()[0]
    f.close()

    f = open("abc.txt", "r")
    audiobooks = int(f.read().splitlines()[0])
    f.close()

    f = open("kymahi.txt", "r")
    kymahi = int(f.read().splitlines()[0])
    f.close()

    f = open("audiobooks.txt", "r")
    audiobooks = int(f.read().splitlines()[0])
    f.close()

@bot.command(name="ip")
async def ip(ctx):
    await ctx.send(get_ip())


async def send_msg(msg: str): 
    await bot.get_channel(1042103392031481858).send(msg)


def get_ip():
    return urlsplit(request.urlopen("http://{}".format(url)).url).netloc


bot.run(token)
