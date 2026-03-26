import discord
import asyncio
from discord.ext import commands, tasks
from datetime import time
import json
import os
from dotenv import load_dotenv
from discord import app_commands

# ─── CARGAR VARIABLES DE ENTORNO ─────────────────────────────
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CANAL_PROGRAMADO_ID = int(os.getenv("ID_CHANNEL"))
USER_KENE = int(os.getenv("ID_USER"))
# ─── CONFIGURACIÓN DEL BOT ───────────────────────────────────
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


# ─── CONTADOR PERSISTENTE ────────────────────────────────────
ARCHIVO_CONTADOR = "daycount.json"

def leer_dia():
    if os.path.exists(ARCHIVO_CONTADOR):
        with open(ARCHIVO_CONTADOR, "r") as f:
            return json.load(f)["dia"]
    return 1

def guardar_dia(dia):
    with open(ARCHIVO_CONTADOR, "w") as f:
        json.dump({"dia": dia}, f)


# ─── EVENTO: Bot listo ───────────────────────────────────────
@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")
    if not os.path.exists(ARCHIVO_CONTADOR):
        guardar_dia(1)
    mensaje_programado.start()


# ─── TAREA PROGRAMADA (cada día a las 9:00 AM UTC) ───────────
#@tasks.loop(time=time(hour=9, minute=0))
# ─── Para pruebas  ─── 
@tasks.loop(seconds=30)
# ─── Para pruebas  ─── 
async def mensaje_programado():
    canal = bot.get_channel(CANAL_PROGRAMADO_ID)
    dia_actual = leer_dia()
    guardar_dia(dia_actual + 1)
    if canal:
        await canal.send(f"📅 Día **{dia_actual}** diciendo pene por cada día que pase hasta que <@{USER_KENE}> prenda stream.")
        for _ in range(dia_actual):
            await canal.send(f"Pene ** x{_+1}**")
            await asyncio.sleep(0.5)
        

# ─── COMANDOS PERSONALIZADOS ─────────────────────────────────
@bot.command(name="hola")
async def hola(ctx):
    await ctx.send(f"👋 ¡Hola, Nigga {ctx.author.mention}!")


@bot.command(name="info")
async def info(ctx):
    servidor = ctx.guild
    await ctx.send(
        f"📊 **{servidor.name}**\n"
        f"👥 Miembros: {servidor.member_count}\n"
        f"📅 Creado: {servidor.created_at.strftime('%d/%m/%Y')}"
    )


@bot.command(name="anuncio")
@commands.has_permissions(administrator=True)
async def anuncio(ctx, *, mensaje):
    await ctx.send(f"📢 **ANUNCIO**\n{mensaje}")


@bot.command(name="modificar_dia")
@commands.has_permissions(administrator=True)
async def modificar_dia(ctx, nuevo_dia: int):
    if nuevo_dia < 1:
        await ctx.send(f"Eche tu eres marica? cómo mondá el día va a ser **{nuevo_dia}????** ❌.")
        return
    guardar_dia(nuevo_dia)
    await ctx.send(f"✅ Aro, ahora el contador estará establecido desde el día **{nuevo_dia}**."
    )
@modificar_dia.error
async def modificar_dia_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("⚠️ Ojo mrk, tienes que poner el día.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f"⚠️ Aja y eso es un día papito lindo?`")

@bot.command(name="consultar_dia")
async def consult_dia(ctx):
    dia_actual = leer_dia()
    await ctx.send(f"joa mrk ya van **{dia_actual}** que el <@{USER_KENE}> no prende :(")

@bot.event
async def on_message(ctx):
    if bot.user.mentioned_in(ctx) and not ctx.author.bot:
        await ctx.channel.send(f"Qué **P E N E ** 🗣🔥🔥 {ctx.author.mention}")
    await bot.process_commands(ctx)  # importante para que los comandos sigan funcionando

import random

@bot.command(name="memide")
async def numero(ctx):
    r= random.random()
    if r < 0.70:
        resultado = random.randint(0, 5)
        mensaje = "🤏 Tan tierno 🤭"
    elif r< 0.95:
        resultado = random.randint(6, 20)
        mensaje = "Qué buena polla tío 🔥🍆"
    else:
        resultado = random.randint(21, 100)
        mensaje= "💀💀💀"
    await ctx.send(f" A {ctx.author.mention} le mide **{resultado}** cm, {mensaje}")
bot.run(TOKEN)
