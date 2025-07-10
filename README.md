# 🤖 HunlarBot

Bu bot, [@HunlarBirligi](https://t.me/HunlarBirligi) kanalına gönderilen mesajları, botun dahil olduğu tüm Telegram gruplarına otomatik olarak iletir.

---

## 🚀 Özellikler

- Kanal postlarını botun bulunduğu gruplara otomatik olarak iletir  
- `/start` ve `/help` komutları ile bilgi verir  
- Grup listesi otomatik olarak tutulur  
- **Sadece bilgi amaçlıdır**, kullanıcı mesajı almaz  
- **Heroku’ya dağıtıma hazırdır**

---

## ☁️ Heroku’ya Tek Tıkla Kurulum

### ⚠️ Not: Bu özelliğin çalışması için GitHub reposunun herkese açık (public) olması gerekir.

Aşağıdaki butona tıklayarak botu Heroku’ya tek tıkla yükleyebilirsin:

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Hunlar/HunlarBot)

> 🔁 Yukarıdaki bağlantı senin `Hunlar/HunlarBot` adlı GitHub adresine özel olarak hazırlanmıştır.

---

## 🔧 Manuel Kurulum

### 1. Telegram Bot oluşturun:
- [@BotFather](https://t.me/BotFather)'dan yeni bir bot oluşturun ve `BOT_TOKEN`'ı alın.

### 2. Heroku ile yükleyin:

```bash
git clone https://github.com/Hunlar/HunlarBot.git
cd HunlarBot
heroku create
heroku config:set BOT_TOKEN=telegram_bot_tokeniniz
git push heroku main
