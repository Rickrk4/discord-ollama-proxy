# This example requires the 'message_content' intent.

import discord
import logging
import ollama
from os import environ as e

print("Starting Discord Proxy Bot...")

# Constants
TOKEN = e.get('DISCORD_TOKEN', None)
OLLAMA_BASE_URL = e.get('OLLAMA_BASE_URL', 'http://localhost:11434')
OLLAMA_MODEL = e.get('OLLAMA_MODEL', 'llama2')
INITIAL_PROMPT =e.get('INITIAL_PROMPT', '') 

RAISE_ON_ERROR = True
LOG_FILE = 'ollama_bot.log'

# Initialization
log_handler = logging.FileHandler(filename=LOG_FILE, encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True

discord_client = discord.Client(intents=intents)
ollama_client = ollama.Client(host=OLLAMA_BASE_URL)
ollama_client.pull(model=OLLAMA_MODEL)

chat_history = {}
prompt = {'role': 'assistant','content': INITIAL_PROMPT,} if INITIAL_PROMPT else None
print(f"Using OLLAMA_BASE_URL: {OLLAMA_BASE_URL}")

def generate_response(history):
    response = ollama_client.chat(model=OLLAMA_MODEL, messages=history)
    return response['message']

async def send_message(message, msg, limit=2000):
    """Send a message to the Discord channel, splitting it if necessary."""
    if len(msg) < limit:
        await message.channel.send(msg)
        return

    msgs = [m.strip(' ') for m in msg.split('.')]
    response = ''
    for m in msgs:
        if len(response) + len(m) > limit:
            await message.channel.send(response)
            response = m + '.'
        else:
            response += m + '.'
    pass

        
@discord_client.event
async def on_ready():
    print(f'Bot connesso come {discord_client.user}')

@discord_client.event
async def on_message(message):
    # Ignora i messaggi dei bot
    if message.author.bot:
        return

    # Controlla se il messaggio è in DM
    if isinstance(message.channel, discord.DMChannel):
        print(f"Messaggio in DM da {message.author}: {message.content}")
        
        # Inizializza la cronologia della chat per l'utente se non esiste
        user_id = str(message.author.id)
        if user_id not in chat_history.keys():
            chat_history[user_id] = [prompt]
            print(f"Nuova cronologia della chat creata per l'utente {user_id}")
            pass
        
        if message.content.lower() == '!reset':
            print(f"Reset della cronologia della chat per l'utente {user_id}")
            chat_history[user_id] = [prompt]
            await send_message(message, "Ohi-ohi, che mal di testa! Devo aver perso la memoria...", limit=1900)
        else:
            chat_history[user_id].append({'role': 'user', 'content': message.content})
            try:
                response = generate_response(chat_history[user_id])
            except Exception as e:
                response = {'role': 'assistant', 'content': "Errore durante la generazione della risposta."}
                if RAISE_ON_ERROR:
                    raise e
                else:
                    print(f"Errore: {e}")
                    pass
            chat_history[user_id].append(response)
            await send_message(message, response['content'], limit=1900)
discord_client.run(TOKEN)