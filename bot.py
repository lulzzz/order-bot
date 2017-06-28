#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
import config
import telebot
import MySQLdb
import random

# Connect to DataBase
db = MySQLdb.connect(host='localhost',user='WRITE YOUR USERNAME', passwd='WRITE YOUR PASSWORD', db='WRITE YOUR DATABASE NAME', charset='utf8')

# Admin settings
admin_username = 'WRITE YOUR USERNAME IN TELEGRAM'
admin_id = 'WRITE YOUR ID IN TELEGRAM'

# Token connect to Bot (change in config.py)
bot = telebot.TeleBot(config.token)

# Cursors
cursor = db.cursor()
cursor2 = db.cursor()

# Global vars
xaccept = False
xwallet = False
xdata = False
xqiwi = False
xyandex = False
xprice = False
xlink = False


# Handler with commands
@bot.message_handler(commands=['start', 'new', 'accept', 'admin', 'setqiwi', 'setyandex', 'setprice', 'wallet', 'data'], func=lambda message: True)
def handle_start(message):
    if message.text == '/start':
        user_markup = telebot.types.ReplyKeyboardMarkup(True)
        user_markup.row('\u270F Order identification')
        user_markup.row('\u267B About the service', '\u26A1 Reviews')
        user_markup.row('/start')

        bot.send_message(message.from_user.id,
                         ''' Hello, <b>%s</b>!\n\n<b>Identification Bot</b> help you in identifying the wallet.'''
                         % message.from_user.first_name,
                         parse_mode="HTML",
                         reply_markup=user_markup)

        sql_start = """REPLACE INTO users (id, first_name, last_name, username)
                    VALUES ('%(id)s', '%(first_name)s', '%(last_name)s', '%(username)s')""" % {
                    "id":message.from_user.id,
                    "first_name":message.from_user.first_name,
                    "last_name":message.from_user.last_name,
                    "username":message.from_user.username}
        cursor.execute(sql_start)
        print (sql_start)
        db.commit()
    # command for new order identification
    if (message.text == '/new') and (message.from_user.username == admin_username):
        sql_newrequest = """SELECT wallet, data, note FROM request WHERE status='0'"""
        cursor.execute(sql_newrequest)
        newrequest = cursor.fetchall()
        for row in newrequest:
            wallet = row[0]
            data = row[1]
            note = row[2]

            print ('Wallet number: ' + str(wallet) + ' | Data: ' + data + ' | Note: ' + str(note))

            bot.send_message(chat_id=admin_id,
                             text="Wallet number: %(wallet)s | Data: %(data)s | Note: %(note)s"
                                  %{"wallet": wallet,
                                    "data": data,
                                    "note": note, })
    # command for accept identification
    if (message.text == '/accept') and (message.from_user.username == admin_username):
        acc_markup = telebot.types.ForceReply(selective=True)
        bot.send_message(message.chat.id, 'Number wallet that has been identified', reply_markup=acc_markup)
        global xaccept
        xaccept = True

    # administrative commands
    if (message.text == '/admin') and (message.from_user.username == admin_username):
        bot.send_message(message.chat.id, '<b>Admin commands:</b>\n\n'
                                          '/new - withdrawal of new orders for identification\n'
                                          '/accept - authentication confirmation\n'
                                          '/setqiwi - update of QIWI number in the requisites\n'
                                          '/setyandex - update of YandexMoney number in the requisites\n'
                                          '/setprice - update price for identification \n', parse_mode="HTML")

    if (message.text == '/setqiwi') and (message.from_user.username == admin_username):
        qiwi_markup = telebot.types.ForceReply(selective=True)
        bot.send_message(message.chat.id, 'Enter a new QIWI number to pay for identification', reply_markup=qiwi_markup)
        #global xaccept
        #global textaccept
        global xqiwi
        xqiwi = True

    if (message.text == '/setyandex') and (message.from_user.username == admin_username):
        yandex_markup = telebot.types.ForceReply(selective=True)
        bot.send_message(message.chat.id, 'Enter a new YandexMoney number to pay for identification', reply_markup=yandex_markup)
        #global xaccept
        #global textaccept
        global xyandex
        xyandex = True

    if (message.text == '/setprice') and (message.from_user.username == admin_username):
        price_markup = telebot.types.ForceReply(selective=True)
        bot.send_message(message.chat.id, 'Enter a new price for the identification service', reply_markup=price_markup)
        #global xaccept
        #global textaccept
        global xprice
        xprice = True

    if message.text == '/wallet':
        markup = telebot.types.ForceReply(selective=False)
        bot.send_message(message.chat.id, 'Enter QIWI, or YandexMoney purse', reply_markup=markup)
        global xwallet
        xwallet = True

    if message.text == '/data':
        markup = telebot.types.ForceReply(selective=False)
        bot.send_message(message.chat.id,
                         'Enter either your passport data for identification, or enter "use the service data""',
                         reply_markup=markup)
        global xdata
        xdata = True

# Handler with messages
@bot.message_handler(func=lambda message: True, content_types=["text"])
def echo_all(message):
    global xwallet
    global xdata
    global wallet
    global xaccept
    global xqiwi
    global xyandex
    global xprice
    global xlink

    if (xqiwi == True):
        xqiwi = False
        qiwi = message.text
        print(message.text)
        sql_setqiwi = """UPDATE head SET qiwi='%(qiwi)s' WHERE id='1'""" % {"qiwi":qiwi}
        cursor.execute(sql_setqiwi)
        db.commit()
        bot.send_message(message.from_user.id, "The QIWI wallet in the details has been successfully changed to<b> %s</b>!" % qiwi, parse_mode="HTML")
        menu_markupacc = telebot.types.ReplyKeyboardMarkup(True)
        menu_markupacc.row('\u270F Order identification')
        menu_markupacc.row('\u267B About the service', '\u26A1 Reviews')
        menu_markupacc.row('/start')
        bot.send_message(message.from_user.id, "\nBefore you the <b>main menu</b> ", reply_markup=menu_markupacc, parse_mode="HTML")

    if (xyandex == True):
        xyandex = False
        yandex = message.text
        print(message.text)
        sql_setyandex = """UPDATE head SET yandex='%(yandex)s' WHERE id='1'""" % {"yandex":yandex}
        cursor.execute(sql_setyandex)
        db.commit()
        bot.send_message(message.from_user.id, "The YandexMoney wallet the details has been successfully changed to<b> %s</b>!" % yandex, parse_mode="HTML")
        menu_markupacc = telebot.types.ReplyKeyboardMarkup(True)
        menu_markupacc.row('\u270F Order identification')
        menu_markupacc.row('\u267B About the service', '\u26A1 Reviews')
        menu_markupacc.row('/start')
        bot.send_message(message.from_user.id, "\nBefore you the <b>main menu</b> ", reply_markup=menu_markupacc,
                         parse_mode="HTML")

    if (xprice == True):
        xprice = False
        price = message.text
        print(message.text)
        sql_setprice = """UPDATE head SET price='%(price)s' WHERE id='1'""" % {"price":price}
        cursor.execute(sql_setprice)
        db.commit()
        bot.send_message(message.from_user.id, "The price of identification has been successfully changed to<b> %s</b>!" % price, parse_mode="HTML")
        menu_markupacc = telebot.types.ReplyKeyboardMarkup(True)
        menu_markupacc.row('\u270F Order identification')
        menu_markupacc.row('\u267B About the service', '\u26A1 Reviews')
        menu_markupacc.row('/start')
        bot.send_message(message.from_user.id, "\nBefore you the <b>main menu</b> ", reply_markup=menu_markupacc,
                         parse_mode="HTML")

    if (xaccept == True):
        xaccept = False
        accept = message.text
        print(message.text)
        if (cursor.execute("""SELECT wallet FROM request WHERE wallet = '%(wallet)s'""" % {"wallet": accept}) == True):
            sql_accwallet = """UPDATE request SET status='1' WHERE wallet='%(wallet)s'""" % {"wallet": accept}
            cursor.execute(sql_accwallet)
            db.commit()
            sql_accmesg = """SELECT chat_id, link FROM request WHERE wallet='%(wallet)s'""" % {"wallet": accept}
            cursor2.execute(sql_accmesg)
            chat_id = cursor2.fetchone()
            #print(chat_id[0])
            menu_markupacc = telebot.types.ReplyKeyboardMarkup(True)
            menu_markupacc.row('\u270F Order identification')
            menu_markupacc.row('\u267B About the service', '\u26A1 Reviews')
            menu_markupacc.row('/start')
            bot.send_message(message.from_user.id, "You have exited the identification confirmation."
                                                   "\nBefore you the <b>main menu</b> ", reply_markup=menu_markupacc, parse_mode="HTML")
            bot.send_message(chat_id=chat_id[0], text="<b>Attention</b>, your wallet has been identified!", parse_mode="HTML")
            xlink = True
        else:
            menu_markupacc = telebot.types.ReplyKeyboardMarkup(True)
            menu_markupacc.row('\u270F Order identification')
            menu_markupacc.row('\u267B About the service', '\u26A1 Reviews')
            menu_markupacc.row('/start')
            bot.send_message(message.from_user.id, "You specified a non-existent wallet in the orders."
                                                   "\nBefore you the <b>main menu</b> ", reply_markup=menu_markupacc, parse_mode="HTML")


    if (xlink == True):
        xlink = False
        link = message.text
        print (link)

    if (xwallet == True):
        xwallet = False
        wallet = message.text
        print('Wallet: ', wallet)

    if (xdata == True):
        xdata = False
        data = message.text
        note = random.randint(0,500)
        print('Data: ', data)
        sql_request = """INSERT INTO request (chat_id, wallet, data, note)
                        VALUES ('%(chat_id)s','%(wallet)s', '%(data)s', '%(note)s')""" % {
                        "chat_id": message.from_user.id,"wallet": wallet, "data": data, "note": note}
        cursor.execute(sql_request)
        db.commit()
        menu_markup = telebot.types.ReplyKeyboardMarkup(True)
        menu_markupacc.row('\u270F Order identification')
        menu_markupacc.row('\u267B About the service', '\u26A1 Reviews')
        menu_markupacc.row('/start')

        sql_infoqiwi = """SELECT qiwi FROM head WHERE ID='1'"""
        cursor.execute(sql_infoqiwi)
        qiwi = cursor.fetchone()
        print (qiwi[0])

        sql_infoyandex = """SELECT yandex FROM head WHERE ID='1'"""
        cursor.execute(sql_infoyandex)
        yandex = cursor.fetchone()
        print(yandex[0])

        sql_infoprice = """SELECT price FROM head WHERE ID='1'"""
        cursor.execute(sql_infoprice)
        price = cursor.fetchone()
        print (price)
        bot.send_message(message.from_user.id, "Pay your order for the amount %(price)s via: \nQIWI: %(qiwi)s \nYandexMoney: %(yandex)s \nwith a note for "
                                               "payment in the form a number: <b>%(note)s</b>." % {"price": price[0], "qiwi": qiwi[0], "yandex": yandex[0], "note": note}, reply_markup=menu_markup, parse_mode="HTML")

    if (message.text == '\u267B About the service'):
        sql_infoservice = """SELECT `info` FROM `settings` WHERE ID='0'"""
        cursor.execute(sql_infoservice)
        infoservice = cursor.fetchone()
        print(infoservice)
        bot.send_message(message.chat.id, "%s" % infoservice, parse_mode="HTML")

    if (message.text == '\u26A1 Reviews'):
        keyboard = telebot.types.InlineKeyboardMarkup()
        url_button = telebot.types.InlineKeyboardButton(
            text="\u25AA github.com",
            url="http://github.com/eorgiose")
        url_button2 = telebot.types.InlineKeyboardButton(
            text="\u25AB link.com",
            url="https://link.com")
        url_button3 = telebot.types.InlineKeyboardButton(
            text="\u25AB link.com", url="http://link.com")
        url_button4 = telebot.types.InlineKeyboardButton(
            text="\u25AA link.com",
            url="http://link.com")
        url_button5 = telebot.types.InlineKeyboardButton(
            text="\u25AA link.com",
            url="http://link.com")
        keyboard.add(url_button, url_button2)
        keyboard.add(url_button3, url_button4)
        keyboard.add(url_button5)
        bot.send_message(message.chat.id, "<pre>About our service are responded to:</pre>", reply_markup=keyboard, parse_mode="HTML")

    if (message.from_user.username == 'admin_username'):
        text = message.text
        sql_chatidusers = """SELECT id FROM users"""
        cursor.execute(sql_chatidusers)
        chat_id = cursor.fetchall()
        i = 0
        print ('Total Row(s):', cursor.rowcount)
        while i < cursor.rowcount:
            print(chat_id[i][0])
            bot.send_message(chat_id=chat_id[i][0], text=text)
            i = i + 1

    if (message.text == '\u270F Order identification'):
        bot.send_message(message.chat.id, text='\u270F You proceeded to create a purse identification order.\n\n'
                                               '\u0031\u20E3 Click on /wallet and enter the QIWI-purse number in the reply message, which is necessary '
                                               'identification, or YandexMoney-purse number, if necessary '
                                               'identification YD.\nAn example of a correct wallet entry: 79997777777\n\n'
                                               '\u0032\u20E3 Click on /data and enter the passport data, for which it is necessary to identify the purse, or enter '
                                               'use the service data so that we identify the wallet according to our data.')

if __name__ == '__main__':
     bot.polling(none_stop=True)