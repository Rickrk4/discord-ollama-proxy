# discord-ollama-proxy
This Python script implements a Discord bot that acts as a proxy to a local language model served by Ollama (e.g., LLaMA 2). Users can interact with the language model by sending direct messages (DMs) to the bot on Discord.

Each user's conversation is completely isolated from others. When a user sends a message to the bot via direct message (DM), a unique chat history is created for them and preserved in memory for the duration of the bot's runtime. This allows for contextual, multi-turn conversations without interference from other users.

If a user wants to start over or clear the ongoing context, they can send the command:  ```!reset```
This command wipes their current chat history and restarts the conversation, optionally reloading the initial prompt if defined.

To connect the bot to your Discord account, you must provide your Discord Bot Token as an environment variable:

```
export DISCORD_TOKEN=your_discord_token_here
```
This token is required for authentication and is specific to your bot application.
You can obtain your bot token by creating an application on the [Discord Developer Portal](https://discord.com/developers/docs/getting-started). For detailed instructions, refer to the official guide:

> **Important:** Never share your bot token publicly or commit it to version control. It gives full control over your bot..



## Installation
```
docker run --rm -d \
  -e DISCORD_TOKEN=your_discord_token \
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
  -e OLLAMA_MODEL=llama2 \ #OPTIONAL 
  -2 INITIAL_PROMPT=your_prompt \ #OPTIONAL
  --name discord-ollama-proxy \
  rickrk4/discord-ollama-proxy
```
