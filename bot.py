import discord
from discord.ext import commands
from discord import app_commands
import pickle
import json

memes = {}
std_cmd = ["add", "del", "help", "commands"]


async def send_message(message, user_message):
    try:
        response = handle_response(user_message)
        if response is not None:
            await message.channel.send(response)
    except Exception as e:
        print(e)

def update_backup():
    with open('commands_data.pkl', 'wb') as f:
        pickle.dump(memes, f)

def load_backup():
    global memes
    try :
        with open('commands_data.pkl', 'rb') as f:
            memes = pickle.load(f)
    except IOError:
        print('no file')


def add_cmd(key, value) -> str:
    global std_cmd
    if key in std_cmd:
        return "Fuck off Zyn :fuck:."
    if memes.get(key) is not None:
        return 'This command already exists with this value : ' + memes[key]
    
    memes[key] = value
    update_backup()
    return 'New command "!'+ key + '" added : ' + value

def del_cmd(key) -> str:
    if memes.get(key) is None:
        return 'There is no command with this name'
    del memes[key]
    update_backup()
    return "Command removed."

def handle_commands() -> str:
    reply = ''
    global std_cmd
    for c in std_cmd :
        reply += f'{c} : usage {"TODO usage"}.\n'
    return reply

def handle_response(msg) -> str:
    msgs = msg.split(' ')

    if memes.get(msgs[0]) is not None:
        return memes[msgs[0]]

    if msgs[0] == 'add':
        return add_cmd(msgs[1], msgs[2])
    
    if msgs[0] == 'del':
        return del_cmd(msgs[1])
    
    if msgs[0] == 'help':
        return 'help'
    
    if msgs[0] == 'commands':
        return handle_commands()

    
def get_token() -> str:
    with open('token.json', 'r') as f :
        data = json.load(f)
    return data["BOT_TOKEN"]

def run_discord_bot():
    load_backup()

    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='$', intents=intents)

    async def fruits_autocomplete(
        interaction: discord.Interaction,
        current: str,
    ) -> list[app_commands.Choice[str]]:
        fruits = ['Banana', 'Pineapple', 'Apple', 'Watermelon', 'Melon', 'Cherry']
        return [
            app_commands.Choice(name=fruit, value=fruit)
            for fruit in fruits if current.lower() in fruit.lower()
        ]
    
    @bot.command()
    @app_commands.autocomplete(item=fruits_autocomplete)
    async def fruits(interaction: discord.Interaction, fruit: str):
        await interaction.response.send_message(f'Your favourite fruit seems to be {fruit}')

    @bot.event
    async def on_ready():
        print(f'{bot.user} is running')

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return
        msg = str(message.content)
        if msg[0] != '!':
            return
        else:
            msg = msg[1:]
            await send_message(message, msg)
    
    bot.run(get_token(), reconnect=False)