# 🤖 HunlarBot

Bu bot, [@HunlarBirligi](https://t.me/HunlarBirligi) kanalına gönderilen mesajları, botun dahil olduğu tüm Telegram gruplarına otomatik olarak iletir.

## 🚀 Özellikler

- Kanal postlarını otomatik olarak gruplara iletir
- `/start` ve `/help` komutları ile bilgi sağlar
- Dinamik olarak botun bulunduğu grupları kaydeder
- Tamamen **bilgi amaçlı** çalışır (interaktif değil)
- **Heroku uyumludur**

---

## ☁️ 1- Heroku'ya Tek Tıkla Kurulum

Aşağıdaki butona tıklayarak Heroku üzerinde kolayca deploy edebilirsin:

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Hunlar/HunlarBot)

📌 Not: Yukarıdaki linkteki `kullaniciadiniz/HunlarBot` kısmını kendi GitHub kullanıcı adı ve repo isminle değiştirmen gerekiyor.

---

## ⚙️ 2- Manuel Kurulum

1. Reponun içindeyken şu adımları izleyin:

```bash
heroku create hunlarbot
heroku config:set BOT_TOKEN=your_telegram_bot_token
git push heroku main# 🤖 HunlarBot

Bu bot, [@HunlarBirligi](https://t.me/HunlarBirligi) kanalına gönderilen mesajları, botun dahil olduğu tüm Telegram gruplarına otomatik olarak iletir.

## 🚀 Özellikler

- Kanal postlarını otomatik olarak gruplara iletir
- `/start` ve `/help` komutları ile bilgi sağlar
- Dinamik olarak botun bulunduğu grupları kaydeder
- Tamamen **bilgi amaçlı** çalışır (interaktif değil)
- **Heroku uyumludur**

---

## ☁️ 1- Heroku'ya Tek Tıkla Kurulum

Aşağıdaki butona tıklayarak Heroku üzerinde kolayca deploy edebilirsin:

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/kullaniciadiniz/HunlarBot)

📌 Not: Yukarıdaki linkteki `kullaniciadiniz/HunlarBot` kısmını kendi GitHub kullanıcı adı ve repo isminle değiştirmen gerekiyor.

---

## ⚙️ 2- Manuel Kurulum

1. Reponun içindeyken şu adımları izleyin:

```bash
heroku create hunlarbot
heroku config:set BOT_TOKEN=your_telegram_bot_token
git push heroku main
