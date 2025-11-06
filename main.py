import os
import random
import logging

import discord
from discord.ext import commands

# ============ LOG AYARI ============
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("LuffyBot")
# ===================================

# ============ BOT AYARLARI ============
intents = discord.Intents.none()
intents.guilds = True
intents.message_content = True  # Bunu Discord Developer Portal'dan da aç!

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
# =======================================


# ============ EVENTLER ============
@bot.event
async def on_ready():
    logger.info(f"Giriş yapıldı: {bot.user} (LuffyBot aktif ✅)")


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    if isinstance(message.channel, discord.DMChannel):
        return

    if message.content.lower().strip() == "sa":
        try:
            cevap = random.choice(SELAM_CEVAPLARI)
            await message.channel.send(cevap)
        except Exception as e:
            logger.error(f"'sa' cevabı atılırken hata: {e}")

    await bot.process_commands(message)
# ==================================


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
# ==================================


# ============ ÇALIŞTIRMA ============
def main():
    # 🔴 TOKEN BURADAN OKUNUYOR
    token = os.getenv("TOKEN")  # Railway'de env olarak ekleyeceğiz

    if not token:
        logger.error("HATA: TOKEN environment variable bulunamadı!")
        return

    try:
        bot.run(token)
    except Exception as e:
        logger.error(f"Bot çalışırken kritik hata: {e}")


if __name__ == "__main__":
    main()
# ==================================
