
# HunlarBot 🤖

Bu bot, @HunlarBirligi kanalına gönderilen mesajları otomatik olarak botun dahil olduğu tüm Telegram gruplarına iletir.

## Özellikler
- Kanal postlarını otomatik iletir
- /start ve /help komutları vardır
- Dinamik olarak grup kaydı yapar
- Heroku'ya uygundur

## Kurulum

1. Bot tokenini [@BotFather](https://t.me/BotFather)'dan al
2. Heroku hesabı oluştur
3. Reponun kök dizinine gel ve şu komutları gir:

```bash
heroku create hunlarbot
heroku config:set BOT_TOKEN=your_bot_token_here
git push heroku main
```

4. Botun çalıştığını kontrol et!

## Ekstra
- Botun düzgün çalışması için hem kanala hem gruplara admin olarak eklenmesi gerekir.
