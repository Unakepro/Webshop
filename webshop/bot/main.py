from webshop.bot.config import TOKEN
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telebot import TeleBot
from webshop.db.models import User, Category, Products, MyCart
from webshop.bot.lookups import category_lookup, separator

start_text = ('Товары со скидкой', 'Категории', 'Моя корзина')

bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def hello(message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(*[KeyboardButton(text=text) for text in start_text])

    if not User.objects(_id=message.from_user.id):
        bot.send_message(message.chat.id, 'Приветствую вас в нашем интернет магазине', reply_markup=kb)
        User.objects.create(_id=message.from_user.id, f_name=message.from_user.first_name)

    else:
        bot.send_message(message.chat.id, f'{message.from_user.first_name} приветствую вас в нашем интернет магазине',
                         reply_markup=kb)


@bot.message_handler(content_types=['text'], func=lambda message: message.text == "Категории")
def categories(message):
    kb = InlineKeyboardMarkup()
    roots = Category.get_root_categories()
    buttons = [InlineKeyboardButton(text=category.title,
                                    callback_data=f'{category_lookup}{separator}{category.id}')
               for category in roots]
    kb.add(*buttons)
    bot.send_message(message.chat.id, text='Выберите категорию', reply_markup=kb)


@bot.callback_query_handler(func=lambda call: call.data.split(separator)[0] == category_lookup)
def category_click(call):
    category_id = call.data.split(separator)[1]
    category = Category.objects.get(id=category_id)
    kb = InlineKeyboardMarkup()

    if category.is_parent:

        subcategory = category.subcategories
        buttons = [InlineKeyboardButton(text=category.title,
                                        callback_data=f'{category_lookup}{separator}{category.id}')
                   for category in subcategory]
        kb.add(*buttons)
        button = InlineKeyboardButton(text="Назад", callback_data=f"{category.title}back")
        kb.add(button)

        bot.edit_message_text(category.title, chat_id=call.message.chat.id,
                              message_id=call.message.message_id, reply_markup=kb)

    else:
        product = category.get_products()

        for i in range(len(product)):
            add_cart = InlineKeyboardMarkup()
            button = InlineKeyboardButton(text="Добавить в корзину", callback_data=f"{product[i].id}_add")
            add_cart.add(button)

            res = product[i].image.read()
            price = product[i].price * (100 - product[i].discount) / 100
            bot.send_photo(call.message.chat.id, res, caption=f'{product[i].title}\n\n'
                                                              f'{product[i].description}\n'
                                                              f'Цена без скидки: {product[i].price}\n\n'
                                                              f'Цена со скидкой: {price}\n', reply_markup=add_cart)

        button = InlineKeyboardButton(text="Назад", callback_data=f"{category.title}back")
        kb.add(button)
        bot.send_message(chat_id=call.message.chat.id, text="Назад", reply_markup=kb)


@bot.message_handler(content_types=['text'], func=lambda message: message.text == "Товары со скидкой")
def sales(message):
    discount = Products.get_discount_products()

    for i in range(len(discount)):
        res = discount[i].image.read()

        kb = InlineKeyboardMarkup()
        button = InlineKeyboardButton(text="Добавить в корзину", callback_data=f"{discount[i].id}_add")
        kb.add(button)

        price = discount[i].price * (100 - discount[i].discount) / 100
        bot.send_photo(message.chat.id, res, caption=f'{discount[i].title}\n\n'
                                                     f'{discount[i].description}\n'
                                                     f'Цена без скидки: {discount[i].price}\n\n'
                                                     f'Цена со скидкой: {price}\n', reply_markup=kb)


@bot.callback_query_handler(func=lambda call: call.data.endswith("back"))
def back(call):
    kb = InlineKeyboardMarkup()

    result = call.data
    result = result[0:-4]

    parent = Category.objects(title=result)[0].parent

    try:
        if parent is None:
            category_one = Category.get_root_categories()
            buttons = [InlineKeyboardButton(text=category.title,
                                            callback_data=f'{category_lookup}{separator}{category.id}')
                       for category in category_one]
            kb.add(*buttons)

        else:
            buttons = [InlineKeyboardButton(text=category.title,
                                            callback_data=f'{category_lookup}{separator}{category.id}')
                       for category in parent.subcategories]
            button = InlineKeyboardButton(text="Назад", callback_data=f"{parent.title}back")
            kb.add(*buttons)
            kb.add(button)

        bot.edit_message_text("Выберите категорию", chat_id=call.message.chat.id,
                              message_id=call.message.message_id, reply_markup=kb)
    except:
        pass


@bot.message_handler(content_types=['text'], func=lambda message: message.text == "Моя корзина")
def my_cart(message):
    carts = MyCart.objects(user_id=message.from_user.id)
    if not carts:
        bot.send_message(chat_id=message.chat.id, text="Нет товаров в корзине")
    else:
        all_price = 0
        for products in carts:
            kb = InlineKeyboardMarkup()

            value = MyCart.objects(product_id=products.product_id)[0].value
            product = Products.objects(id=products.product_id)
            if value > 0:
                button = InlineKeyboardButton(text="Удалить", callback_data=f"{product[0].id}_delete")
                button1 = InlineKeyboardButton(text="+1", callback_data=f"{product[0].id}_+1")
                button2 = InlineKeyboardButton(text=f"-1", callback_data=f"{product[0].id}_-1")
                kb.add(button2, button, button1)

                res = product[0].image.read()
                price = product[0].price * (100 - product[0].discount) / 100
                all_price += (price * value)

                bot.send_photo(message.chat.id, res, caption=f'{product[0].title}\n\n'
                                                             f'{product[0].description}\n\n'
                                                             f'{Category.objects(title="Routers")[0].id}'
                                                             f'Количество товаров: {value}\n'
                                                             f'Цена без скидки: {product[0].price}\n\n'
                                                             f'Цена со скидкой: {price}\n', reply_markup=kb)
            else:
                pass
        if all_price > 0:
            key = InlineKeyboardMarkup()
            done = InlineKeyboardMarkup()

            button = InlineKeyboardButton(text="Очистить корзину", callback_data=f"delete_cart")
            done_button = InlineKeyboardButton(text="Оформить заказ", callback_data="done")

            key.add(button)
            done.add(done_button)

            bot.send_message(chat_id=message.chat.id, text="Очистить корзину", reply_markup=key)
            bot.send_message(chat_id=message.chat.id, text="Общая цена:")
            bot.send_message(chat_id=message.chat.id, text=all_price, reply_markup=done)
        else:
            bot.send_message(chat_id=message.chat.id, text="Нет товаров в корзине")


@bot.callback_query_handler(func=lambda call: call.data.endswith("_add"))
def add_my_cart(call):
    product_id = call.data
    product_id = product_id[0:-4]

    if not MyCart.objects(user_id=call.from_user.id, product_id=product_id):
        MyCart.objects.create(user_id=call.from_user.id, product_id=product_id)
        bot.answer_callback_query(callback_query_id=call.id, text="Товар успешно добавлен в корзину",
                                  show_alert=False)
    else:
        MyCart.objects(user_id=call.from_user.id, product_id=product_id).update(inc__value=1)
        bot.answer_callback_query(callback_query_id=call.id, text="Товар успешно добавлен в корзину",
                                  show_alert=False)


@bot.callback_query_handler(func=lambda call: call.data.endswith("_delete"))
def delete_item(call):
    product_id = call.data
    product_id = product_id[0:-7]

    MyCart.objects(product_id=product_id).delete()
    bot.answer_callback_query(callback_query_id=call.id, text="Товар удален из корзины",
                              show_alert=False)


@bot.callback_query_handler(func=lambda call: call.data == "delete_cart")
def delete_cart(call):
    res = MyCart.objects(user_id=call.from_user.id)

    res.delete()
    bot.answer_callback_query(callback_query_id=call.id, text="Корзина пуста",
                              show_alert=True)


@bot.callback_query_handler(func=lambda call: call.data.endswith("_+1"))
def add_one(call):
    add_id = call.data[0:-3]
    MyCart.objects(product_id=add_id).update(inc__value=1)
    bot.answer_callback_query(callback_query_id=call.id, text="Товара на 1 больше",
                              show_alert=False)


@bot.callback_query_handler(func=lambda call: call.data.endswith("_-1"))
def minus_one(call):
    add_id = call.data[0:-3]
    try:
        if MyCart.objects(product_id=add_id)[0].value < 1:
            bot.answer_callback_query(callback_query_id=call.id, text="Товара нет в корзине",
                                      show_alert=False)
        else:
            MyCart.objects(product_id=add_id).update(dec__value=1)
            bot.answer_callback_query(callback_query_id=call.id, text="Товара на 1 меньше",
                                      show_alert=False)
    except:
        bot.answer_callback_query(callback_query_id=call.id, text="Товара нет в корзине",
                                  show_alert=False)


@bot.callback_query_handler(func=lambda call: call.data == "done")
def save_cart(call):
    if User.objects(_id=call.from_user.id)[0].surname is None:
        User.objects(_id=call.from_user.id).update(push__add_price=float(call.message.json['text']))
        surname = bot.send_message(chat_id=call.message.chat.id, text="Введите свою фамилию")

        bot.register_next_step_handler(surname, get_surname)

    else:
        User.objects(_id=call.from_user.id).update(push__add_price=float(call.message.json['text']))

        res = MyCart.objects(user_id=call.from_user.id)
        res.delete()
        bot.send_message(chat_id=call.message.chat.id, text="С вами свяжется оператор, ожидайте")


def get_surname(message):
    User.objects(_id=message.from_user.id).update(surname=message.json['text'])
    email = bot.send_message(chat_id=message.chat.id, text="Введите свою емейл")
    bot.register_next_step_handler(email, get_email)


def get_email(message):
    User.objects(_id=message.from_user.id).update(email=message.json['text'])

    res = MyCart.objects(user_id=message.from_user.id)
    res.delete()
    bot.send_message(chat_id=message.chat.id, text="С вами свяжется оператор, ожидайте")


def start_bot():
    bot.infinity_polling()
