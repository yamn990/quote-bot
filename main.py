from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
import openai
import logging

# مفاتيح الوصول
TELEGRAM_TOKEN = "7012024373:AAESP_3pUKCS5LiRyzSpDrmIo9W_hGTMMnc"
OPENAI_API_KEY = "ضع_هنا_API_KEY_الخاصة_بك_من_OpenAI"

# إعداد البوت و Flask
bot = Bot(token=TELEGRAM_TOKEN)
app = Flask(__name__)
dispatcher = Dispatcher(bot, None, workers=0)
openai.api_key = OPENAI_API_KEY

# تسجيل الأخطاء
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# توليد اقتباس من ChatGPT
def generate_quote(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "أنت كاتب اقتباسات عربي محترف."},
                {"role": "user", "content": f"اكتب اقتباسًا رائعًا حول: {prompt}"}
            ],
            temperature=0.9
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"حدث خطأ: {str(e)}"

# أمر /start
def start(update, context):
    update.message.reply_text("👋 أهلًا بك في بوت الاقتباسات. فقط أرسل لي موضوعًا، وسأكتب لك اقتباسًا ملهمًا!")

# التعامل مع الرسائل النصية
def handle_message(update, context):
    user_input = update.message.text
    quote = generate_quote(user_input)
    update.message.reply_text(quote)

# ربط الأوامر
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

# Webhook
@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

# الصفحة الرئيسية
@app.route("/")
def home():
    return "بوت الاقتباسات جاهز!"

# تشغيل الخادم
if __name__ == "__main__":
    app.run(port=5000)
