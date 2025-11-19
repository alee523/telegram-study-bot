from flask import Flask, request
from telebot import TeleBot, types
import telebot

# Flask App
app = Flask(__name__)

# توكن البوت
TOKEN = "7249425290:AAH3XBcTzvwY4akfpAeXxBVqWYES5OZHwQo"
bot = TeleBot(TOKEN)

# زر الرجوع
BACK_BUTTON = "🔙 رجوع"

# هيكل المواد والدروس
subjects = {
    "📘 مادة الإحصاء": ["الكتاب الإلكتروني", "المحاضرات", "واجبات", "امتحانات"],
    "📗 مادة الموائع": ["الكتاب الإلكتروني", "المحاضرات", "واجبات", "امتحانات"],
    "📙 مادة الهيدرولوجيا": ["الكتاب الإلكتروني", "المحاضرات", "واجبات", "امتحانات"],
    "📒 مادة القياسات": ["الكتاب الإلكتروني", "المحاضرات", "واجبات", "امتحانات"],
    "📕 مادة التحليل": ["الكتاب الإلكتروني", "المحاضرات", "واجبات", "امتحانات"],
    "📓 مادة هندسة الحفر (موارد)": ["الكتاب الإلكتروني", "المحاضرات", "واجبات", "امتحانات"],
    "📔 مادة الكيمياء البيئية (بيئية)": ["الكتاب الإلكتروني", "المحاضرات", "واجبات", "امتحانات"],
    "📚 مادة الإستشعار": ["الكتاب الإلكتروني", "المحاضرات", "واجبات", "امتحانات"],
    "📜 مادة جيولوجيا": ["الكتاب الإلكتروني", "المحاضرات", "واجبات", "امتحانات"],
    "🩺 مادة الصحة والسلامة": ["الكتاب الإلكتروني", "المحاضرات", "واجبات", "امتحانات"]
}

# تفرّعات المحاضرات
lectures = ["PDF", "فيديوهات", "صوتيات"]

# محتويات المواد
contents = {
    "📘 مادة الإحصاء": {
        "الكتاب الإلكتروني": "",
        "PDF": {"المحاضرة الأولى": "", "المحاضرة الثانية": ""},
        "فيديوهات": {"المحاضرة الأولى": "", "المحاضرة الثانية": ""},
        "صوتيات": {"المحاضرة الأولى": "", "المحاضرة الثانية": ""},
        "واجبات": "",
        "امتحانات": ""
    },

    # باقي المواد بنفس التنسيق …

    "🩺 مادة الصحة والسلامة": {
        "الكتاب الإلكتروني": "",
        "PDF": {
            "المحاضرة الأولى": "https://drive.google.com/file/d/14QJmp2ft_EC5C2y3OabM6u0abyHaSo3h/view?usp=drivesdk",
            "المحاضرة الثانية": ""
        },
        "فيديوهات": {"المحاضرة الأولى": "", "المحاضرة الثانية": ""},
        "صوتيات": {"المحاضرة الأولى": "", "المحاضرة الثانية": ""},
        "واجبات": {
            "واجب متجاوب": "https://drive.google.com/file/d/1p8Qlp_yfFcb4CdSmX_LBLLHwhOqRIyhU/view?usp=drivesdk",
            "واجب PDF": "https://drive.google.com/file/d/1RhPuWdUY6h4Q5WThICawvvmaqVasnjeE/view?usp=drivesdk"
        },
        "امتحانات": ""
    }
}

# حالة المستخدمين
user_state = {}

# القوائم
def main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for subject in subjects.keys():
        markup.add(types.KeyboardButton(subject))
    bot.send_message(message.chat.id, "📚 اختر المادة الدراسية:", reply_markup=markup)
    user_state[message.chat.id] = {"level": "main", "subject": None, "sub": None}

def subject_menu(message, subject):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for item in subjects[subject]:
        markup.add(types.KeyboardButton(item))
    markup.add(types.KeyboardButton(BACK_BUTTON))
    bot.send_message(message.chat.id, f"📖 اختر من {subject}:", reply_markup=markup)
    user_state[message.chat.id] = {"level": "subject", "subject": subject, "sub": None}

def lectures_menu(message, subject):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for lec in lectures:
        markup.add(types.KeyboardButton(lec))
    markup.add(types.KeyboardButton(BACK_BUTTON))
    bot.send_message(message.chat.id, f"📚 اختر نوع المحاضرات:", reply_markup=markup)
    user_state[message.chat.id]["level"] = "lectures"

def lessons_menu(message, subject, lec_type):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for lesson in contents[subject][lec_type]:
        markup.add(types.KeyboardButton(lesson))
    markup.add(types.KeyboardButton(BACK_BUTTON))
    bot.send_message(message.chat.id, f"📚 اختر {lec_type}:", reply_markup=markup)
    user_state[message.chat.id]["level"] = "lessons"
    user_state[message.chat.id]["sub"] = lec_type

# إرسال المحتوى
def send_content(chat_id, link):
    if link.startswith("http"):
        bot.send_message(chat_id, f"📄 <a href='{link}'>اضغط هنا لفتح المحتوى</a>", parse_mode="HTML")
    elif link:
        bot.send_document(chat_id, open(link, "rb"))
    else:
        bot.send_message(chat_id, "🚫 المحتوى غير متاح حالياً.")

# /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "مرحبًا! 👋\nأنا بوت Water 🌊 & Environment Study Bot.")
    main_menu(message)

# كل الأزرار
@bot.message_handler(func=lambda m: True)
def handle_buttons(message):
    chat_id = message.chat.id
    text = message.text
    state = user_state.get(chat_id, {"level": "main", "subject": None, "sub": None})

    # زر الرجوع
    if text == BACK_BUTTON:
        if state["level"] == "subject":
            main_menu(message)
        elif state["level"] == "lectures":
            subject_menu(message, state["subject"])
        elif state["level"] in ["lessons", "assignments"]:
            lectures_menu(message, state["subject"])
        return

    # اختيار مادة
    if text in subjects:
        subject_menu(message, text)
        return

    # داخل مادة
    if state["level"] == "subject":
        subject = state["subject"]

        if text == "الكتاب الإلكتروني":
            send_content(chat_id, contents[subject]["الكتاب الإلكتروني"])
            return

        if text == "المحاضرات":
            lectures_menu(message, subject)
            return

        if text == "واجبات":
            assignments = contents[subject]["واجبات"]
            if isinstance(assignments, dict):
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                for a in assignments:
                    markup.add(types.KeyboardButton(a))
                markup.add(types.KeyboardButton(BACK_BUTTON))
                bot.send_message(chat_id, "📄 اختر الواجب:", reply_markup=markup)
                user_state[chat_id]["level"] = "assignments"
            else:
                send_content(chat_id, assignments)
            return

        if text == "امتحانات":
            send_content(chat_id, contents[subject]["امتحانات"])
            return

    # اختيار نوع محاضرات
    if state["level"] == "lectures":
        subject = state["subject"]
        if text in lectures:
            lessons_menu(message, subject, text)
        return

    # اختيار محاضرة
    if state["level"] == "lessons":
        subject = state["subject"]
        lec_type = state["sub"]
        if text in contents[subject][lec_type]:
            send_content(chat_id, contents[subject][lec_type][text])
        return

    # اختيار واجب
    if state["level"] == "assignments":
        subject = state["subject"]
        link = contents[subject]["واجبات"].get(text)
        send_content(chat_id, link)
        return

# ====================== Webhook ======================
@app.route(f"/{TOKEN}", methods=['POST'])
def webhook():
    json_update = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_update)
    bot.process_new_updates([update])
    return "OK", 200

# مسار تشغيل لفحص السيرفر
@app.route("/")
def index():
    return "Bot running!", 200