import discord
import pickle
import json
import streamlit as st

commands = {}

async def send_message(message, user_message):
    try:
        response = handle_response(user_message)
        if response != None:
            await message.channel.send(response)
    except Exception as e:
        print(e)

def update_backup():
    with open('commands_data.pkl', 'wb') as f:
        pickle.dump(commands, f)

def load_backup():
    global commands
    try :
        with open('commands_data.pkl', 'rb') as f:
            commands = pickle.load(f)
    except IOError:
        print('no file')


def add_cmd(key, value) -> str:
    if commands.get(key) != None:
        return 'This command already exists with this value : ' + commands[key]
    
    commands[key] = value
    update_backup()
    return 'New command "!'+ key + '" added : ' + value

def del_cmd(key) -> str:
    if commands.get(key) == None:
        return 'There is no command with this name'
    del commands[key]
    update_backup()
    return "Command removed."


def handle_response(msg) -> str:
    msgs = msg.split(' ')

    if commands.get(msgs[0]) != None:
        return commands[msgs[0]]

    if msgs[0] == 'add':
        return add_cmd(msgs[1], msgs[2])
    
    if msgs[0] == 'del':
        return del_cmd(msgs[1])
    
    if msgs[0] == 'help':
        return 'help'    

    
def get_token() -> str:
    return st.secrets["TOKEN"]
    """
    with open('token.json', 'r') as f :
        data = json.load(f)
    return data["BOT_TOKEN"]
    """

def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents = intents)
    load_backup()

    @client.event
    async def on_ready():
        print(f'{client.user} is running')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        msg = str(message.content)

        if msg[0] != '!':
            return
        else:
            msg = msg[1:]
            await send_message(message, msg)
    
    client.run(get_token())
