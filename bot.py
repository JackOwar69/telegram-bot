import asyncio
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "7999264768:AAEDkV5IO-sq1UG0SaiOBWxiQUkP32vFdk8"

user_state = {}
user_level = {}
users = set()
user_start_time = {}

# ========= MILD =========
mild_images = [
    "https://files.catbox.moe/slhbet.jpg",
    "https://files.catbox.moe/un4tgg.jpg",
    "https://files.catbox.moe/2wty9k.jpg",
    "https://files.catbox.moe/bnx7sm.jpg",
]
mild_audio = "https://files.catbox.moe/qykkz8.mp3"

# ========= MODERATE =========
moderate_pdf = "https://files.catbox.moe/i0cep7.pdf"
moderate_audio = "https://files.catbox.moe/vzc8em.mp3"

# ========= SEVERE =========
severe_image = "https://files.catbox.moe/wo1dn6.jpg"
severe_audio = "https://files.catbox.moe/s29ndu.mp3"


# ========== LEVEL TEXT ==========
def level_message(level):

    if level == "mild":
        return """ممتاز! مستواك الحالي يسمح لك بالتحصيل العالي. إليك نصائح للحفاظ على هذا الهدوء
قبل المذاكرة:
خطوات سريعة:

اجلس بشكل مستقيم وأرخِ كتفيك
خذ 3 أنفاس ببطء:
شهيق 4 ثواني
حبس 2 ثانية
زفير 6 ثواني
سؤال توجيهي:

ماذا أتذكر بالفعل عن هذا الموضوع؟

إعادة صياغة التفكير:

بدل: "ممكن أنسى كل حاجة"
قل: "أنا فاكر أكتر مما أعتقد"

اتجاه المذاكرة:

راجع النقاط الأساسية فقط
لا تبدأ موضوعات جديدة
اختبر نفسك (Active Recall)
حدّد 3 أهداف فقط لكل جلسة 
راجع عناوين الموضوع أولًا 
أثناء المذاكرة:
استخدم Active Recall 
اكتب ملخص سريع بيدك 
اربط المعلومات بحالات تمريض (clinical cases) 
قبل الامتحان:
نم 6–8 ساعات 
راجع النقاط الأساسية فقط"""

    if level == "moderate":
        return """بدأ التوتر يتسلل إليك؟ لا تقلق، لنعد معاً لمسار التركيز. جرب هذه التقنيات الآن
1-تقنية التأريض (5-4-3-2-1)

✋ 5 أشياء يمكنك رؤيتها
🖐️ 4 أشياء يمكنك لمسها
👂 3 أشياء يمكنك سماعها
👃 شيئان يمكنك شمهما
👅 شيء واحد يمكنك تذوقه

2-تنظيم التنفس:
شهيق 4 ثواني
حبس 4 ثواني
زفير 4 ثواني
كرر 5 مرات

3-إعادة صياغة التفكير:
بدل: "هسقط"
قل: "هجاوب سؤال واحد في كل مرة"

4-استراتيجية المهام الصغيرة:
اختر موضوع واحد
ذاكر 10 دقائق فقط
راحة 2 دقيقة
كرر"""

    if level == "severe":
        return "تم تفعيل وضع التهدئة"

    return ""


# ========== DAILY CHECKER ==========
async def daily_checker(context: ContextTypes.DEFAULT_TYPE):

    now = time.time()

    text = """Daily Follow-up

هل مارست تمارين التهدئة اليوم؟
مستوى القلق اليوم (0–10)"""

    for chat_id in list(users):

        start_time = user_start_time.get(chat_id)

        if not start_time:
            continue

        if now - start_time >= 86400:

            try:
                await context.bot.send_message(chat_id=chat_id, text=text)
                user_state[chat_id] = "daily"
                user_start_time[chat_id] = now
            except Exception as e:
                print("DAILY ERROR:", e)


# ========== SEND LEVEL ==========
async def send_level(update: Update, context: ContextTypes.DEFAULT_TYPE, level):

    chat_id = update.effective_chat.id

    if level == "mild":
        for img in mild_images:
            try:
                await context.bot.send_photo(chat_id=chat_id, photo=img)
            except:
                pass

        await context.bot.send_audio(chat_id=chat_id, audio=mild_audio)
        await context.bot.send_message(chat_id=chat_id, text=level_message("mild"))
        return

    if level == "moderate":
        await context.bot.send_audio(chat_id=chat_id, audio=moderate_audio)
        await context.bot.send_message(chat_id=chat_id, text=level_message("moderate"))

        try:
            await context.bot.send_document(
                chat_id=chat_id,
                document=moderate_pdf,
                filename="moderate.pdf"
            )
        except:
            pass
        return

    if level == "severe":
        try:
            await context.bot.send_photo(chat_id=chat_id, photo=severe_image)
        except:
            pass

        await asyncio.sleep(0.5)

        await context.bot.send_audio(chat_id=chat_id, audio=severe_audio)

        messages = [
            "الهدف: خفض ضربات القلب",
            "توقف عن المذاكرة الآن",
            "تنفس ببطء",
            "أنت في أمان"
        ]

        for msg in messages:
            await context.bot.send_message(chat_id=chat_id, text=msg)

        return


# ========== START ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id
    users.add(chat_id)

    user_state[update.effective_user.id] = "init"

    user_start_time[chat_id] = time.time()

    await update.message.reply_text(
        "افتح الاستبيان واحسب درجات كل سؤال ثم اكتب: خلصت\n\n"
        "📘 English Form:\n"
        "https://docs.google.com/forms/d/e/1FAIpQLSd-kqkRqY9nEbST5BY2cvw5gV0lep3dqFOvVUcp_aEZm4QQ/viewform\n\n"
        "📗 النموذج العربي:\n"
        "https://docs.google.com/forms/d/e/1FAIpQLSf0TuKM9c31iRYwsGCNrUR18WA2uMqhyQOuUcZHmMx2KteTmA/viewform?usp=publish-editor"
    )


# ========== MAIN ==========
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    text = update.message.text.strip()

    users.add(chat_id)

    state = user_state.get(user_id, "init")

    if state == "score":

        if not text.isdigit():
            await update.message.reply_text("اكتب رقم فقط من 0 إلى 21")
            return

        score = int(text)

        if score <= 9:
            level = "mild"
        elif score <= 14:
            level = "moderate"
        else:
            level = "severe"

        user_level[user_id] = level
        user_state[user_id] = "mood"

        await send_level(update, context, level)

        await update.message.reply_text(
            "كيف تشعر الآن؟\n1-أفضل\n2-كما أنا\n3-أسوأ"
        )
        return

    if state == "daily":

        if not text.isdigit():
            await update.message.reply_text("اكتب رقم من 0 إلى 10 فقط")
            return

        score = int(text)

        if score <= 9:
            level = "mild"
        elif score <= 14:
            level = "moderate"
        else:
            level = "severe"

        user_level[user_id] = level
        user_state[user_id] = "mood"

        await send_level(update, context, level)
        return

    if text == "خلصت":
        user_state[user_id] = "score"
        await update.message.reply_text("اكتب نتيجتك من 0 إلى 21")
        return

    if state == "mood":

        current = user_level.get(user_id, "mild")

        if text == "1":
            await update.message.reply_text("جيد. استمر على نفس الخطوات")
            return

        if text == "2":
            await send_level(update, context, current)
            return

        if text == "3":

            new = "moderate" if current == "mild" else "severe"
            user_level[user_id] = new
            await send_level(update, context, new)

            if new == "severe":
                await update.message.reply_text("يفضل التحدث مع مختص نفسي أو مرشد جامعي")

            return


# ========== RUN ==========
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

# ✅ FIXED JOBQUEUE ISSUE
job_queue = app.job_queue
job_queue.run_repeating(daily_checker, interval=60, first=10)

print("Bot running...")
app.run_polling()
