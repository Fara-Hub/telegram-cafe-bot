from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler
)
from datetime import datetime
import pytz

# ВСТАВЬ сюда свой токен и chat_id
TOKEN = "7794922900:AAHDKyZxn1PN6gMujKML1CD4DLBPljM2H_k"
ADMIN_CHAT_ID =  5702266078

LANG_SELECT, CATEGORY, ITEM = range(3)

# Часовой пояс Москвы
MOSCOW_TZ = pytz.timezone('Europe/Moscow')

# Функция проверки рабочего времени кафе
def is_cafe_open():
    now = datetime.now(MOSCOW_TZ)
    current_hour = now.hour
    return 11 <= current_hour < 24

# Стоп-лист (список недоступных позиций)
stop_list = []

MESSAGES = {
    "start": "👋 Добро пожаловать в кафе САМОНИ!",
    "choose_category": "Выберите категорию:",
    "choose_dish": "Выберите блюдо:",
    "item_added": "✅ *{}* добавлено в корзину.",
    "cart_empty": "🛒 Корзина пуста.",
    "thank_you": "Спасибо за заказ! ❤️",
    "back": "⬅️ Назад",
    "cart": "🛒 Посмотреть корзину",
    "order_done": "✅ Оформить заказ"
}

CATEGORY_ICONS = {
    "🍲 Супы": "🍲",
    "🥟 Выпечка и закуски": "🥟",
    "🔥 Горячие блюда": "🔥",
    "🍢 Шашлык": "🍢",
    "🥗 Салаты": "🥗",
    "🥣 Соусы": "🥣",
    "🥤 Напитки": "🥤"
}

MENU = {
    "🍲 Супы": {
        "Шурпа с говядиной": 290,
        "Фатир шурпа": 350,
        "Лагман": 300,
        "Мастава": 260,
        "Чучвара": 300,
        "Манты шурпа": 310
    },
    "🥟 Выпечка и закуски": {
        "Самса (курица)": 100,
        "Самса (говядина)": 110,
        "Самса (баранина)": 120,
        "Лепешка": 30,
        "Фагир": 60,
        "Чак-чак": 130,
        "Наггетсы (6шт)": 180,
        "Фри": 150
    },
    "🔥 Горячие блюда": {
        "САДЖ (курица)": 950,
        "САДЖ (говядина)": 1000,
        "САДЖ (баранина)": 1250,
        "Манты": 300,
        "Плов": 300,
        "Дулма": 300,
        "Жаркое (говядина)": 440,
        "Жаркое (курица)": 400,
        "Лагман жареный": 420,
        "Хинкали (1шт)": 80,
        "Овощная гриль": 250,
        "Курутоб (курица)": 380,
        "Курутоб (говядина)": 400,
        "Мясо с грибами": 480,
        "Крылья хрустящие (6шт)": 280,
        "Аджапсандал с говядиной": 430
    },
    "🍢 Шашлык": {
        "Люля-кебаб (говядина)": 390,
        "Люля-кебаб (баранина)": 410,
        "Баранина корейка": 540,
        "Баранина мякоть": 480,
        "Курица": 380,
        "Сёмга": 750,
        "Дородо": 720,
        "Форель": 580,
        "Шашлык ассорти": 2350,
        "Куриные крылышки": 320,
        "Хан кебаб": 380,
        "Баранний микс": 570
    },
    "🥗 Салаты": {
        "Брынза нарезка": 250,
        "Ачу-чучик": 150,
        "Солёная нарезка": 200,
        "Овощная нарезка": 200,
        "Цезарь": 280,
        "Оливье": 240,
        "Сомони": 310,
        "Мясной": 320,
        "Букет зелень": 230,
        "Греческий": 260,
        "Мангал салат": 300
    },
    "🥣 Соусы": {
        "Красный": 35,
        "Чесночный": 35,
        "Чака": 40,
        "Перец халапеньо": 35
    },
    "🥤 Напитки": {
        "Добрый Кола (0,5 л)": 100,
        "Добрый Кола (1 л)": 140,
        "Кока-Кола (1 л)": 140,
        "RC Cola (1 л)": 200,
        "Burn": 150,
        "Адреналин": 150,
        "Monster": 90,
        "Drive": 100,
        "Lipton": 100,
        "Мохито Ачалуки": 100,
        "Обычная вода (0,5 л)": 45,
        "Обычная вода (1,25 л)": 80,
        "Обычная вода (2 л)": 140
    },
"🌯 Шаурма": {
        "Стандарт (курица)": 250,
        "Стандарт (говядина)": 290,
        "Стандарт (баранина)": 300,
        "Большая (курица)": 270,
        "Большая (говядина)": 320,
        "Большая (баранина)": 350,
        "Цезарь (курица)": 260,
        "Цезарь (говядина)": 300,
        "Цезарь (баранина)": 340,
        "Чизбургерная (курица)": 310,
        "Чизбургерная (говядина)": 340,
        "Чизбургерная (баранина)": 380,
        "Острая": 285,
        "Шаурм Дог": 220,
        "С наггетсами": 250,
        "Мясная": 400,
        "Вегетарианская": 200,
        "Картошка фри (курица)": 265,
        "Картошка фри (люля)": 310,
        "Картошка фри (говядина)": 340,
        "Гирос (курица)": 270,
        "Гирос (люля)": 320,
        "Гирос (говядина)": 350,
        "Терияки (курица)": 290,
        "Терияки (люля)": 320,
        "Терияки (говядина)": 370
    },
    "🍔 Фастфуд": {
        "Хот-дог классический": 179,
        "Хот-дог двойной": 179,
        "Картошка по-деревенски": 180,
        "Картошка фри": 150,
        "Крылья (4шт)": 199,
        "Крылья (8шт)": 360,
        "Наггетсы (6шт)": 180,
        "Фри бойс": 280,
        "Двойное мясо": 140,
        "Грибы шампиньоны": 75,
        "Перец халапеньо": 35
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_cafe_open():
        await update.message.reply_text("Кафе закрыто. Мы работаем с 11:00 до 00:00 по московскому времени.")
        return ConversationHandler.END
    context.user_data["cart"] = {}
    keyboard = [[KeyboardButton(cat)] for cat in MENU.keys()]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        MESSAGES["start"],
        reply_markup=reply_markup
    )
    return CATEGORY

async def show_categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_cafe_open():
        await update.message.reply_text("Кафе закрыто. Мы работаем с 11:00 до 00:00 по московскому времени.")
        return ConversationHandler.END
    keyboard = [[KeyboardButton(cat)] for cat in MENU.keys()]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        MESSAGES["choose_category"],
        reply_markup=reply_markup
    )
    return CATEGORY

async def show_items(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_cafe_open():
        await update.message.reply_text("Кафе закрыто. Мы работаем с 11:00 до 00:00 по московскому времени.")
        return ConversationHandler.END
    category = update.message.text

    if category not in MENU:
        await update.message.reply_text(MESSAGES["choose_category"])
        return CATEGORY

    context.user_data["category"] = category

    icon = CATEGORY_ICONS.get(category, "")
    available_items = {k: v for k, v in MENU[category].items() if k not in stop_list}
    if not available_items:
        await update.message.reply_text("К сожалению, все позиции в стоп-листе.")
        return CATEGORY

    text = f"{icon} *{category}*\n\n"
    for dish, price in available_items.items():
        text += f"• {dish} — {price} ₽\n"

    buttons = [[KeyboardButton(dish)] for dish in available_items.keys()]
    buttons.append([KeyboardButton(MESSAGES["back"])])
    buttons.append([KeyboardButton(MESSAGES["order_done"])])
    buttons.append([KeyboardButton(MESSAGES["cart"])])

    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )
    return ITEM

async def choose_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_cafe_open():
        await update.message.reply_text("Кафе закрыто. Мы работаем с 11:00 до 00:00 по московскому времени.")
        return ConversationHandler.END
    text = update.message.text

    if text == MESSAGES["back"]:
        return await show_categories(update, context)

    if text == MESSAGES["order_done"]:
        return await finish_order(update, context)

    if text == MESSAGES["cart"]:
        return await show_cart(update, context)

    category = context.user_data.get("category")
    if category and text in MENU[category] and text not in stop_list:
        price = MENU[category][text]
        await add_to_cart(update, context, text, price)
        return ITEM
    else:
        await update.message.reply_text(MESSAGES["choose_dish"])
        return ITEM

async def add_to_cart(update: Update, context: ContextTypes.DEFAULT_TYPE, item_name: str, price: int):
    cart = context.user_data.setdefault('cart', {})
    if item_name in cart:
        cart[item_name]['quantity'] += 1
    else:
        cart[item_name] = {'quantity': 1, 'price': price}
    await update.message.reply_text(MESSAGES["item_added"].format(item_name), parse_mode="Markdown")

async def show_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_cafe_open():
        await update.message.reply_text("Кафе закрыто. Мы работаем с 11:00 до 00:00 по московскому времени.")
        return ConversationHandler.END
    cart = context.user_data.get('cart', {})

    if not cart:
        await update.message.reply_text(MESSAGES["cart_empty"])
        return ITEM

    items_text = []
    total = 0
    for item, data in cart.items():
        item_total = data['quantity'] * data['price']
        items_text.append(f"▪ {item} × {data['quantity']} = {item_total}₽")
        total += item_total

    response = (
        "🛒 *Ваш заказ:*\n\n" +
        "\n".join(items_text) +
        f"\n\n💵 *Итого:* {total}₽\n\n"
        "Выберите действие:\n"
        "/add_more - Добавить товары\n"
        "/clear_cart - Очистить корзину\n"
        "/checkout - Оформить заказ"
    )

    await update.message.reply_text(response, parse_mode="Markdown")
    return ITEM

async def clear_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["cart"] = {}
    await update.message.reply_text("🗑️ Корзина очищена.")
    return await show_categories(update, context)

async def finish_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_cafe_open():
        await update.message.reply_text("Кафе закрыто. Мы работаем с 11:00 до 00:00 по московскому времени.")
        return ConversationHandler.END
    cart = context.user_data.get('cart', {})

    if not cart:
        await update.message.reply_text(MESSAGES["cart_empty"])
        return ConversationHandler.END

    text = ""
    total = 0
    for item, data in cart.items():
        subtotal = data['quantity'] * data['price']
        text += f"• {item} × {data['quantity']} = {subtotal} ₽\n"
        total += subtotal

    order_summary = f"🧾 *Ваш заказ:*\n{text}\n*Итого:* {total} ₽"
    await update.message.reply_text(order_summary, parse_mode="Markdown")

    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"📥 Новый заказ:\n\n{text}\nИтого: {total} ₽",
        parse_mode="Markdown"
    )

    context.user_data["cart"] = {}
    await update.message.reply_text(MESSAGES["thank_you"])
    return ConversationHandler.END

async def handle_cart_actions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command = update.message.text.lower()
    if command == '/add_more':
        return await show_categories(update, context)
    elif command == '/clear_cart':
        return await clear_cart(update, context)
    elif command == '/checkout':
        return await finish_order(update, context)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚫 Заказ отменён.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, show_items)],
            ITEM: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_item)]
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            CommandHandler("cart", show_cart),
            CommandHandler("add_more", show_categories),
            CommandHandler("clear_cart", clear_cart),
            CommandHandler("checkout", finish_order),
        ]
    )

    app.add_handler(conv)
    app.add_handler(MessageHandler(filters.COMMAND, handle_cart_actions))
    app.run_polling()

if __name__ == "__main__":
    main()

# 👇 ЭТО ВНИЗУ bot.py, для "обмана" Railway
try:
    from flask import Flask
    app = Flask(__name__)

    @app.route('/')
    def home():
        return "Bot is running!"

except:
    pass

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
