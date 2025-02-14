import discord
import asyncio
import re
import os

CHANNEL_ID = 1340074598330535957
DEFAULT_DELAY = 18000

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


def parse_time(time_str):
    matches = re.findall(r'(\d+)([smh])', time_str.lower())
    if not matches:
        return None

    total_seconds = 0
    for value, unit in matches:
        if unit == 's':  # Segundos
            total_seconds += int(value)
        elif unit == 'm':  # Minutos
            total_seconds += int(value) * 60
        elif unit == 'h':  # Horas
            total_seconds += int(value) * 3600

    return total_seconds


@client.event
async def on_ready():
    print(f'Bot conectado como {client.user}')

    channel = client.get_channel(CHANNEL_ID)

    if channel:
        guild_name = channel.guild.name
        print(f"Bot está conectado ao servidor: {guild_name}")

        if not channel.permissions_for(channel.guild.me).send_messages and not channel.permissions_for(channel.guild.me).manage_messages:
            print(
                "Erro: O bot não tem permissão para enviar mensagens ou gerenciar mensagens neste canal.")
    else:
        print(f"Canal com ID {CHANNEL_ID} não encontrado.")


@client.event
async def on_message(message):
    if message.channel.id == CHANNEL_ID:
        if client.user in message.mentions:
            await message.reply(
                "🤖 **Como eu funciono:**\n"
                "1. Envie uma mensagem e ela será por padrão removida após {18000}s.\n"
                "\n"
                "ou...\n"
                "1. Envie uma mensagem no formato `XhYmZs Sua mensagem` (ex: `1m30s Olá!`).\n"
                "2. Eu apago a mensagem após o tempo especificado.\n"
                "3. Você recebe uma confirmação temporária com o tempo de duração.\n"
                "**Exemplos:**\n"
                "- `10s Teste` → Mensagem apagada após 10 segundos.\n"
                "- `2m30s Mensagem longa` → Apagada após 2 minutos e 30 segundos.\n"
                "- `1h Duração longa` → Apagada após 1 hora."
            )
            return

        if message.author == client.user:
            return

        content = message.content
        time_match = re.match(r'^(\d+[smh]+)\s*', content.lower())

        delay = DEFAULT_DELAY

        if time_match:
            time_str = time_match.group(1)
            delay = parse_time(time_str)
            if delay is None:
                delay = DEFAULT_DELAY

        try:
            await asyncio.sleep(delay)
            await message.delete()
            print(
                f'Mensagem de {message.author} apagada após {delay} segundos.')
        except discord.Forbidden:
            print(f"Erro: O bot não tem permissão para apagar mensagens no canal.")
        except discord.NotFound:
            print(f"Erro: A mensagem não foi encontrada (já foi apagada?).")
        except Exception as e:
            print(f"Erro inesperado ao apagar a mensagem: {e}")

# Inicia o bot
client.run(os.getenv("TOKEN"))
