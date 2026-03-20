import discord
from discord.ext import commands, tasks
import asyncio
from datetime import time

# Configuración
TOKEN = "TU_TOKEN_AQUÍ"
CANAL_PROGRAMADO_ID = 123456789  # ID del canal donde enviar mensajes automáticos

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


# ─── EVENTO: Bot listo ───────────────────────────────────────
@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")
    mensaje_programado.start()  # Inicia la tarea programada


# ─── TAREA PROGRAMADA (cada día a las 9:00 AM) ───────────────
@tasks.loop(time=time(hour=9, minute=0))  # Hora UTC
async def mensaje_programado():
    canal = bot.get_channel(CANAL_PROGRAMADO_ID)
    if canal:
        await canal.send("🌅 ¡Buenos días! Mensaje automático del bot.")


# ─── COMANDOS PERSONALIZADOS ──────────────────────────────────

@bot.command(name="hola")
async def hola(ctx):
    """Saluda al usuario"""
    await ctx.send(f"👋 ¡Hola, {ctx.author.mention}!")


@bot.command(name="info")
async def info(ctx):
    """Muestra info del servidor"""
    servidor = ctx.guild
    await ctx.send(
        f"📊 **{servidor.name}**\n"
        f"👥 Miembros: {servidor.member_count}\n"
        f"📅 Creado: {servidor.created_at.strftime('%d/%m/%Y')}"
    )


@bot.command(name="anuncio")
@commands.has_permissions(administrator=True)
async def anuncio(ctx, *, mensaje):
    """Envía un anuncio (solo admins). Uso: !anuncio <texto>"""
    await ctx.send(f"📢 **ANUNCIO**\n{mensaje}")


# ─── INICIAR BOT ──────────────────────────────────────────────
bot.run(TOKEN)