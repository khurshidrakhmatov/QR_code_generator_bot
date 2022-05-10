from lib2to3.pgen2 import token
import telebot
import qrcode
import sqlite3
from telebot import types
from pyzbar.pyzbar import decode
from PIL import Image


token = '5073339010:AAFN2VWKx4w84w8RF2RyOb-sxHchM24Bwu0'
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("ℹ️ About us ℹ️")
    btn2 = types.KeyboardButton("Qr Code generate")
    btn3 = types.KeyboardButton("Scan Qr Qode")

    markup.add(btn2, btn3)
    markup.add(btn1)



    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(id TEXT)""")

    connect.commit()

        # check id in fields

    people_id = message.chat.id

    people_id = message.chat.id
    cursor.execute(f"SELECT id FROM login_id WHERE id = {people_id}")
    data = cursor.fetchone()
    if data is None:
            # add values in fields
        user_id = [message.chat.id]
        cursor.execute("INSERT INTO login_id VALUES(?);", user_id)
        connect.commit()

        bot.send_message(message.chat.id,'Hello, {0.first_name}, Welcome to QrCode Creating bot  '.format(message.from_user),reply_markup=markup)

    elif message.from_user.username == 'Cyber_defender1':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("ℹ️ About us ℹ️")
        btn2 = types.KeyboardButton("Qr Code generate")
        btn3 = types.KeyboardButton("Scan Qr Qode")
        btn4 = types.KeyboardButton("static")

        markup.add(btn1,btn2)
        markup.add(btn3, btn4)

        bot.send_message(message.chat.id, "Hello admin", reply_markup=markup)

    else:
        bot.send_message(message.chat.id, 'Hello, {0.first_name}, Welcome to QrCode Creating bot  '.format(message.from_user),reply_markup=markup)


@bot.message_handler(content_types=['text'])
def starter(message):
    if message.text == "ℹ️ About us ℹ️":
        bot.send_message(message.chat.id, "Hello, and welcome to the QrCode creation bot.\nthe bot was created by  \n@Cyber_defender1")

    elif message.text == "Qr Code generate":
        msg = bot.send_message(message.chat.id, 'please send me a word or link')
        bot.register_next_step_handler(msg, qr_create)

    elif message.text == "Scan Qr Qode":
        msg = bot.send_message(message.chat.id, "please send me a picture with qr code")
        bot.register_next_step_handler(msg, scan)
    elif message.text == "static":
        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()

        data = cursor.execute("SELECT id FROM login_id")

        data = data.fetchall()
        ln = len(data)
        bot.send_message(message.chat.id,f"Пользователи: {ln}")



def qr_create(message):

    name = "qr.png"
    img = qrcode.make(message.text)
    img.save(name)

    photo = open("qr.png", 'rb')
    bot.send_photo(message.chat.id, photo, "your Qr Code")


def scan(message):

    try:


        file_info = bot.get_file(message.photo[len(message.photo)-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src='scan.png';
        with open(src, 'wb') as new_file:
           new_file.write(downloaded_file)

        d = decode(Image.open('scan.png'))
        bot.send_message(message.chat.id,d[0].data.decode())

    except Exception as e:
            msg = bot.reply_to(message, '☝️ this is not a picture\n\npreesed "Scan Qr Code"')


bot.infinity_polling()