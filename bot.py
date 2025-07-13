import logging
import os
import asyncio
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes,
    CallbackQueryHandler, MessageHandler, filters
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Ayasofya gif URL'si
AYASOFYA_GIF = "https://i.imgur.com/RlhMceQ.gif"

# Destek ve Zeyd butonları için Telegram kullanıcı adları
DESTEK_GRUBU = "@Kizilsancaktr"
ZEYD_BIN_SABR = "@zeydbinhalit"

# Kur'an API URL'leri
API_SURELER = "https://api.acikkuran.com/v2/sureler"
API_AYET = "https://api.acikkuran.com/v2/ayet"
API_AYET_RANDOM = "https://api.acikkuran.com/v2/ayet/random"

# Hadisler JSON dosyası yolu
HADISLER_JSON_PATH = "hadisler.json"

# Ezan Vakitleri API (örnek)
EZAN_API_URL = "https://api.collectapi.com/pray/all?data.city="  # Sonuna şehir adı eklenir
EZAN_API_KEY = os.getenv("EZAN_API_KEY")  # CollectAPI için API anahtarınız

# Grup ID - buraya grubun Telegram chat ID'si konmalı
GRUP_ID = os.getenv("GROUP_CHAT_ID")  # t.me/cemaatsohbet'in chat_id değeri

# Komut: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    # Sadece özelden değil, gruplardan da mesaj gelirse cevap versin:
    keyboard = [
        [InlineKeyboardButton("Destek Grubu", url=f"https://t.me/{DESTEK_GRUBU.lstrip('@')}")],
        [InlineKeyboardButton("ZEYD BİN SABR", url=f"https://t.me/{ZEYD_BIN_SABR.lstrip('@')}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        # Fotoğraf yerine gif gönderiyoruz
        await context.bot.send_animation(
            chat_id=chat_id,
            animation=AYASOFYA_GIF,
            caption=(
                "Bu bot Hayatın Yoğun Temposuna Kur'an'ı Kerim'i ve İslamiyeti "
                "Hatırlatmak ve yaymak amacıyla yapılmıştır."
            ),
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Start komutunda hata: {e}")
        await update.message.reply_text(
            "Bu bot Hayatın Yoğun Temposuna Kur'an'ı Kerim'i ve İslamiyeti Hatırlatmak ve yaymak amacıyla yapılmıştır."
        )

# Komut: /ayet (rastgele ayet getirir)
async def ayet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        res = requests.get(API_AYET_RANDOM)
        res.raise_for_status()
        data = res.json()

        ayet_arapca = data.get("data", {}).get("text", "Arapça metin bulunamadı.")
        ayet_meal = data.get("data", {}).get("meali", "Meal bulunamadı.")
        sure_adi = data.get("data", {}).get("sure", {}).get("name", "Sure ismi yok")
        ayet_no = data.get("data", {}).get("numberInSurah", "N/A")

        mesaj = f"📖 <b>{sure_adi} {ayet_no}. Ayet</b>\n\n{ayet_arapca}\n\n📝 Meal:\n{ayet_meal}"
        await update.message.reply_text(mesaj, parse_mode='HTML')

    except Exception as e:
        logger.error(f"/ayet komutunda hata: {e}")
        await update.message.reply_text("Ayet getirirken hata oluştu.")

# Komut: /ara {ayet veya sure ismi}
async def ara(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Lütfen bir ayet ya da sure ismi yazınız. Örnek: /ara Fatiha")
        return

    sorgu = " ".join(context.args).strip()
    try:
        # Öncelikle sureler arasında arama yapalım
        res = requests.get(API_SURELER)
        res.raise_for_status()
        sureler = res.json().get("data", [])

        # Girilen sorgu ile eşleşen sure bulunacak
        bulunan_sure = None
        for sure in sureler:
            if sorgu.lower() == sure.get("name", "").lower() or sorgu.lower() == sure.get("nameTr", "").lower():
                bulunan_sure = sure
                break

        if bulunan_sure:
            # Bulunan surenin tüm ayetleri çekilecek
            sure_no = bulunan_sure.get("number")
            ayetler_res = requests.get(f"https://api.acikkuran.com/v2/sureler/{sure_no}/ayetler")
            ayetler_res.raise_for_status()
            ayetler = ayetler_res.json().get("data", [])

            mesaj = f"📖 <b>{bulunan_sure.get('nameTr')} ({bulunan_sure.get('name')}) Sure'si</b>\n\n"
            for ayet in ayetler[:10]:  # İlk 10 ayet gösteriliyor
                mesaj += f"{ayet.get('numberInSurah')}. Ayet: {ayet.get('text')}\nMeal: {ayet.get('meali')}\n\n"

            await update.message.reply_text(mesaj, parse_mode='HTML')
            return

        else:
            # Sure bulunamadıysa ayet ismi veya numarasına göre arama yapalım
            # Bu API böyle ayet ismiyle değil, sure ve ayet numarası ile çalışıyor.
            # Biz basitçe ayet numarası yoksa hata veriyoruz.
            await update.message.reply_text("Lütfen sure ismi yazınız. Ayet ismi ile arama desteklenmiyor.")
            return

    except Exception as e:
        logger.error(f"/ara komutunda hata: {e}")
        await update.message.reply_text("Arama yapılırken hata oluştu.")

# Komut: /hadis (rastgele hadis getirir)
import json
import random

async def hadis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open(HADISLER_JSON_PATH, "r", encoding="utf-8") as f:
            hadisler = json.load(f)

        hadis_secimi = random.choice(hadisler)
        metin = hadis_secimi.get("hadis", "Hadis metni bulunamadı.")
        kaynak = hadis_secimi.get("kaynak", "Kaynak belirtilmemiş.")

        mesaj = f"📜 Hadis:\n{metin}\n\n📚 Kaynak: {kaynak}"
        await update.message.reply_text(mesaj)

    except Exception as e:
        logger.error(f"/hadis komutunda hata: {e}")
        await update.message.reply_text("Hadis getirilirken hata oluştu.")

# Ezan vakti mesajı atma fonksiyonu (örnek, şehir ve vakit bilgisi alır)
async def ezan_vakti_mesaj_gonder(context: ContextTypes.DEFAULT_TYPE):
    try:
        sehir = "Istanbul"  # Burayı istediğin şehir ile değiştir
        headers = {"Authorization": EZAN_API_KEY}
        res = requests.get(EZAN_API_URL + sehir, headers=headers)
        res.raise_for_status()
        data = res.json()

        # Örnek veri yapısına göre (CollectAPI örneği)
        # data['result'][0]['times'] içinde vakitler var
        # Bu örnek basittir, gerçek API cevabına göre güncelleme gerekebilir.

        vakitler = data.get("result", [{}])[0].get("times", {})
        # Bu örnek sadece sabah vakti kontrolü
        sabah_vakti = vakitler.get("Imsak", None)
        if sabah_vakti:
            mesaj = f"{sehir} için Sabah (İmsak) namaz vakti geldi."
            await context.bot.send_message(chat_id=GRUP_ID, text=mesaj)

    except Exception as e:
        logger.error(f"Ezan vakti mesajında hata: {e}")

# Bot ana fonksiyon
async def main():
    TOKEN = os.getenv("TOKEN")
    if not TOKEN:
        logger.error("TOKEN environment variable not set!")
        return

    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ayet", ayet))
    application.add_handler(CommandHandler("ara", ara))
    application.add_handler(CommandHandler("hadis", hadis))

    # Ezan vakti mesajları için zamanlama (örnek: her saat başı)
    # Daha gelişmiş zamanlama ve vakit takibi için APScheduler veya benzeri kullanılabilir.
    # Burada basit örnek:
    async def ezan_vakti_loop():
        while True:
            await ezan_vakti_mesaj_gonder(application)
            await asyncio.sleep(3600)  # Her saat başı çalışır

    application.job_queue.run_once(lambda ctx: asyncio.create_task(ezan_vakti_loop()), when=0)

    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
