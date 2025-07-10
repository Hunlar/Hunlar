
import os
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.environ.get("BOT_TOKEN")
KANAL_USERNAME = "HunlarBirligi"
GRUP_KAYIT_DOSYASI = "gruplar.json"

def gruplari_yukle():
    if os.path.exists(GRUP_KAYIT_DOSYASI):
        with open(GRUP_KAYIT_DOSYASI, "r") as f:
            return set(json.load(f))
    return set()

def gruplari_kaydet(gruplar):
    with open(GRUP_KAYIT_DOSYASI, "w") as f:
        json.dump(list(gruplar), f)

aktif_gruplar = gruplari_yukle()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mesaj = (
        "Hun İmparatorluğu Federasyonuna Bağlı Ülkeler için yapılacak ortak çalışmalar için "
        "botun her gruba dahil olması gerekmektedir.\n\n"
        "Ülkelerin İsimleri : Özbekistan, Pakistan, Arabistan, Suriye, Almanya, Kıbrıs, "
        "Türkmenistan, BAE, Kırgızistan.\n\n"
        "Bu bot, İmparatorluk adına tüm ticari anlaşmalar çerçevesinde gerekli parayı "
        "kripto yoluyla aktarım için yapılmıştır."
    )
    await update.message.reply_text(mesaj)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mesaj = (
        "Gerekli kişiye yardım için bilgi verilmiştir.\n"
        "İmparatorluk size desteklerini sağlayacaktır."
    )
    await update.message.reply_text(mesaj)

async def yeni_grup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat.type in ["group", "supergroup"]:
        if chat.id not in aktif_gruplar:
            aktif_gruplar.add(chat.id)
            gruplari_kaydet(aktif_gruplar)
            print(f"Yeni grup eklendi: {chat.title} ({chat.id})")

async def kanal_mesaji(update: Update, context: ContextTypes.DEFAULT_TYPE):
    channel_post = update.channel_post
    if channel_post.chat.username == KANAL_USERNAME:
        for grup_id in aktif_gruplar:
            try:
                await context.bot.copy_message(
                    chat_id=grup_id,
                    from_chat_id=channel_post.chat.id,
                    message_id=channel_post.message_id
                )
            except Exception as e:
                print(f"Mesaj gönderilemedi -> {grup_id}: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.ChatType.GROUPS, yeni_grup))
    app.add_handler(MessageHandler(filters.ChannelPost, kanal_mesaji))

    print("HunlarBot çalışıyor...")
    app.run_polling()
