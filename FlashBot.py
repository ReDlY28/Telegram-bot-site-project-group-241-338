import os
import telebot
from telebot import types
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("❌ Не найден BOT_TOKEN в .env файле.")

bot = telebot.TeleBot(BOT_TOKEN)

# Советы / полезные ссылки
info_links = {
    "🎯 AIM и тренировки": [
        ("ВСЕ ПРО АИМ В КС2 ЗА 15 МИНУТ", "https://www.youtube.com/watch?v=ep7MVCF3F-s&t=374s&ab_channel=Kuro"),
        ("ВСЕ ПРО МУВМЕНТ В КС2 ЗА 15 МИНУТ", "https://www.youtube.com/watch?v=cLlxteZOzgQ&t=4s&ab_channel=Kuro"),
        ("Cybershoke тренировки", "https://cybershoke.net/ru/cs2")
    ],
    "🧠 Советы от PRO": [
        ("ГЛАВНЫЕ ОШИБКИ ВСЕХ ИГРОКОВ В CS2 ОТ 4,000ELO", "https://www.youtube.com/watch?v=EVBNfb8KnwY&ab_channel=%D0%9C%D1%8D%D0%B9")
    ],
    "📊 Статистика": [
        ("Статистика вашего аккаунта CS2", "https://csstats.gg/")
    ],
    "🎮 Начать играть": [
        ("CS2 в Steam", "https://store.steampowered.com/app/730/CounterStrike_2/")
    ],
    "💼 Скины и торговля": [
        ("ВСЁ ПРО ФЛОАТЫ СКИНОВ В CS2", "https://www.youtube.com/watch?v=riAq0T4qozQ&ab_channel=RepublicGame"),
        ("Купить скины на CS.MONEY", "https://cs.money/"),
        ("Купить скины на Market.CSGO", "https://market.csgo.com/")
    ],
    "🧷 Бинды": [
        ("Полный гайд по биндам от про игроков в CS2", "https://www.youtube.com/watch?v=EuNIlsTW1q8&ab_channel=Sparkius")
    ]
}

# Квизы
quiz_questions = [
    {
        "question": "Сколько максимум игроков может быть в команде в матчмейкинге CS2?",
        "options": ["3", "5", "6", "8"],
        "answer": "5"
    },
    {
        "question": "Какая карта отсутствует в маппуле CS2?",
        "options": ["Dust2", "Inferno", "Nuke", "Train"],
        "answer": "Train"
    },
    {
        "question": "Сколько стоит AWP в CS2?",
        "options": ["4750", "5000", "5250", "4000"],
        "answer": "4750"
    },
    {
        "question": "Какой клавишей по умолчанию бросается граната?",
        "options": ["G", "F", "Mouse1", "Mouse2"],
        "answer": "Mouse1"
    }
]

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        "Добро пожаловать в FlashBaron Бота 🎮\n"
        "Здесь ты найдёшь:\n\n"
        "✅ Полезные советы по тренировкам и аиму\n"
        "✅ Ссылки на скины и торговые площадки\n"
        "✅ Сайты для отслеживания статистики\n"
        "✅ Крутые видео с геймплеем и лайфхаками\n"
        "✅ Квиз по CS2 для проверки своих знаний\n"
        "✅ Последние обновления CS2\n\n"
        "🛠 Используй команду /help, чтобы увидеть все доступные команды."
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="HTML")
    
# Команда /help
@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = (
        "🤖 <b>Доступные команды:</b>\n"
        "/help — показать список команд\n"
        "/tips — советы, обучение и полезные ссылки\n"
        "/quiz — сыграть в квиз по CS2\n"
        "/update — новости и обновления\n"
        "/links — ссылки на площадки, скины, Steam"
    )
    bot.send_message(message.chat.id, help_text, parse_mode="HTML")

# Команда /tips
@bot.message_handler(commands=['tips'])
def send_tips(message):
    for category, links in info_links.items():
        text = f"<b>{category}</b>\n"
        for title, url in links:
            text += f"• <a href='{url}'>{title}</a>\n"
        bot.send_message(message.chat.id, text, parse_mode="HTML")

# Команда /quiz
@bot.message_handler(commands=['quiz'])
def start_quiz(message):
    user_data[message.chat.id] = {"quiz_index": 0, "score": 0}
    send_quiz_question(message.chat.id)

def send_quiz_question(chat_id):
    data = user_data[chat_id]
    index = data["quiz_index"]

    if index >= len(quiz_questions):
        score = data["score"]
        bot.send_message(chat_id, f"🏁 Викторина окончена! Ваш результат: {score}/{len(quiz_questions)}")
        return

    q = quiz_questions[index]
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for option in q["options"]:
        markup.add(option)

    msg = bot.send_message(chat_id, f"❓ {q['question']}", reply_markup=markup)
    bot.register_next_step_handler(msg, process_answer)

def process_answer(message):
    data = user_data[message.chat.id]
    index = data["quiz_index"]
    q = quiz_questions[index]

    if message.text == q["answer"]:
        data["score"] += 1
        bot.send_message(message.chat.id, "✅ Верно!")
    else:
        bot.send_message(message.chat.id, f"❌ Неверно. Правильный ответ: {q['answer']}")

    data["quiz_index"] += 1
    send_quiz_question(message.chat.id)

# Команда /update
@bot.message_handler(commands=['update'])
def send_updates(message):
    updates = (
        
        
        "🆕 <b>Последние обновления CS2</b>\n"
        "• Добавлены новые карты.\n"
        "• Добавлена награда за задания и система заданий.\n"
        "• Решена проблема, из-за которой прогресс миссии отображался обнулённым при переподключении к идущему матч.\n"
        "• Grail: Карта обновлена до последней версии из мастерской.\n"
        "• Решена проблема, из-за которой огонь был виден сквозь дым.\n"
        "• Внесены различные исправления и улучшения, связанные со звуками интерфейса.\n"
        "• Устранены причины сбоев и повышена стабильность.\n"

    )
    bot.send_message(message.chat.id, updates, parse_mode="HTML")

# Команда /links
@bot.message_handler(commands=['links'])
def send_links(message):
    links_text = (
        "🔗 <b>Полезные ссылки</b>\n"
        "• <a href='https://store.steampowered.com/app/730/CounterStrike_2/'>CS2 в Steam</a>\n"
        "• <a href='https://csstats.gg/'>Статистика игроков CS2</a>\n"
        "• <a href='https://market.csgo.com/'>Market.CSGO</a>\n"
        "• <a href='https://cs.money/'>CS.MONEY</a>\n"
        "• <a href='https://cybershoke.net/ru/cs2'>Cybershoke — тренировочный сервер</a>"
    )
    bot.send_message(message.chat.id, links_text, parse_mode="HTML")

# Хранилище данных
user_data = {}

# Запуск бота
bot.infinity_polling()
