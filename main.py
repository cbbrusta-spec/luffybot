import os
import random
import logging
from threading import Thread

import discord
from discord.ext import commands
from flask import Flask

# ============ LOG AYARI ============
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("LuffyBot")
# ===================================


# ============ FLASK KEEP-ALIVE (RENDER İÇİN) ============
app = Flask(__name__)

@app.route("/")
def home():
    return "LuffyBot is alive!"

def run_web():
    # Render ortamı PORT değişkenini otomatik veriyor
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=run_web, daemon=True)
    t.start()
# ========================================================


# ============ DISCORD BOT AYARLARI ============

# ÖNEMLİ: default() kullanıyoruz, böylece message intent vs. açık geliyor
intents = discord.Intents.default()
intents.message_content = True  # mesaj içeriğini okuyabilsin

bot = commands.Bot(
    command_prefix=".",
    intents=intents,
    help_command=None
)

SELAM_CEVAPLARI = [
    "selam moruk 😎",
    "naber yavrum 💀",
    "naber aşkım 😏",
    "selam kanki 👋",
    "napıyon lan 😂",
    "hoş geldin reis 🤙",
    "ooo kimler gelmiş 😈",
    "as as kardeşim 🧠",
    "selam paşam 👑",
    "gönüllerin korsanı LuffyBot burada ☠️"
]
# ========================================================


# ============ EVENTLER ============
@bot.event
async def on_ready():
    logger.info(f"Giriş yapıldı: {bot.user} (LuffyBot aktif ✅)")
    try:
        await bot.change_presence(activity=discord.Game(name=".help yaz 🧠"))
    except Exception as e:
        logger.error(f"Presence ayarlanırken hata: {e}")


@bot.event
async def on_message(message: discord.Message):
    # Botların mesajını görmezden gel
    if message.author.bot:
        return

    # DM mesajlarını şimdilik yok say
    if isinstance(message.channel, discord.DMChannel):
        return

    # Debug istersen açarsın:
    # logger.info(f"Mesaj geldi: {message.content} | Kanal: {message.channel} | Kullanıcı: {message.author}")

    # "sa" yazılınca cevap ver
    if message.content.lower().strip() == "sa":
        try:
            cevap = random.choice(SELAM_CEVAPLARI)
            await message.channel.send(cevap)
        except Exception as e:
            logger.error(f"'sa' cevabı atılırken hata: {e}")

    # Komutların da çalışması için
    await bot.process_commands(message)
# ========================================================


# ============ KOMUTLAR ============
@bot.command()
async def ping(ctx: commands.Context):
    """Botun çalışıp çalışmadığını kontrol eder."""
    try:
        await ctx.send("Yaşıyorum moruk, LuffyBot çevrimiçi 🧠")
    except Exception as e:
        logger.error(f".ping komutunda hata: {e}")


@bot.command(name="help")
async def help_command(ctx: commands.Context):
    """Kullanılabilen komutları gösterir."""
    metin = (
        "**LuffyBot Komutları**\n"
        "`.ping` → Botun çalıştığını kontrol eder.\n"
        "`sa` yaz → LuffyBot random selam versin.\n"
    )
    try:
        await ctx.send(metin)
    except Exception as e:
        logger.error(f".help komutunda hata: {e}")
# ========================================================


# ============ ÇALIŞTIRMA ============
def main():
    # Render port uyarısı için Flask web sunucusunu başlat
    keep_alive()

    # TOKEN'i ortam değişkeninden al
    token = os.getenv("TOKEN")

    if not token:
        logger.error(
            "HATA: TOKEN environment variable bulunamadı! "
            "Render → Environment kısmına Key=TOKEN, Value=Discord bot token'in ekli olmalı."
        )
        return

    try:
        bot.run(token)
    except Exception as e:
        logger.error(f"Bot çalışırken kritik hata: {e}")


if __name__ == "__main__":
    main()
# ========================================================
