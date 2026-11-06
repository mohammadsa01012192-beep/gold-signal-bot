import os
import json
import urllib.request
import urllib.parse

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()


def telegram_api(method, data=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/{method}"

    if data:
        encoded = urllib.parse.urlencode(data).encode("utf-8")
        request = urllib.request.Request(url, data=encoded)
    else:
        request = urllib.request.Request(url)

    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def send_message(chat_id, text):
    return telegram_api(
        "sendMessage",
        {
            "chat_id": chat_id,
            "text": text,
        },
    )


def handle_message(message):
    chat_id = message["chat"]["id"]
    text = message.get("text", "").strip()

    if text == "/start":
        send_message(
            chat_id,
            "🥇 ربات Gold Signal M5 فعال شد.\n\n"
            "وضعیت: آماده\n"
            "بازار: XAUUSD\n"
            "تایم‌فریم اصلی: M5\n"
            "تأیید روند: M15\n\n"
            "فعلاً فقط ارسال سیگنال فعال است."
        )

    elif text == "/status":
        send_message(
            chat_id,
            "✅ ربات فعال است.\n"
            "⏳ موتور تحلیل بازار در مرحله اتصال به داده‌های قیمت است."
        )

    elif text == "/help":
        send_message(
            chat_id,
            "دستورات:\n\n"
            "/start - شروع ربات\n"
            "/status - وضعیت ربات\n"
            "/help - راهنما"
        )

    else:
        send_message(
            chat_id,
            "دستور شناخته نشد.\n"
            "برای راهنما /help را بزن."
        )


def main():
    if not BOT_TOKEN:
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN تنظیم نشده است."
        )

    print("Gold Signal M5 is running...")

    offset = None

    while True:
        try:
            data = {
                "timeout": 30,
            }

            if offset is not None:
                data["offset"] = offset

            result = telegram_api("getUpdates", data)

            for update in result.get("result", []):
                offset = update["update_id"] + 1

                message = update.get("message")

                if message:
                    handle_message(message)

        except Exception as error:
            print("Error:", error)


if __name__ == "__main__":
    main()
