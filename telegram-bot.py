import telebot#import library to work with telegram bots
import config#import bot configuration settings
from telebot import types#work with keyboard and buttons
import requests#library to parse sites
import datetime#library to work with dates
from difflib import SequenceMatcher#library to check is 2 strings are similar
#check similarity percentage of two strings
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

users_language = 0 #varibale, which i use to define users's language
bot = telebot.TeleBot(config.TOKEN)

#start command
@bot.message_handler(commands = ['start'])
def start(message):
    global users_language#text depends on users's language. By default it's English
    if users_language == 0:
        bot.send_message(message.chat.id,"Hello!")
        bot.send_message(message.chat.id,"Choose /language to choose your language. And use /help to get the list of commands. \nIf you have any troubles use /author to get author's contacts.")
    else:
        bot.send_message(message.chat.id, "Привет!")
        bot.send_message(message.chat.id, "Используй /language,чтобы выбрать свой язык. И используй /help,чтобы получить список комманд. \nЕcли у Вас возникли какие-либо проблемы, тогда используйте /author, чтобы получить контакты автора.")

#get the list of commands
@bot.message_handler(commands=['help'])
def help(message):
    if users_language==0:
        bot.send_message(message.chat.id,"/language -- set your native language \n/vaccine -- get the list of places in your region, where you can made a vaccine (only in Belarus) \n/stat -- get statistics of coronavirus cases around the world \n/help -- get the full list of commands \n/author -- get author's contacts")
    else:
        bot.send_message(message.chat.id, "/language -- установить свой родной язык \n/vaccine -- получить список мест в вашей области, где Вы можете сделать вакцину (только в Беларуси) \n/stat -- получить статистику по коронавирусу по всему миру \n/help --  получить полный список комманд \n/author -- получить контакты автора")

#change language
@bot.message_handler(commands=['language'])
def language(message):
    global users_language
    lang_keyboard = types.InlineKeyboardMarkup()
    en_button = types.InlineKeyboardButton(text="English", callback_data="english")
    rus_button = types.InlineKeyboardButton(text="Русский", callback_data="russian")
    lang_keyboard.add(en_button, rus_button)
    if users_language==0:
        bot.send_message(message.chat.id, "Choose your language.",reply_markup=lang_keyboard)
    else:
        bot.send_message(message.chat.id, "Выберите свой язык.",reply_markup=lang_keyboard)

    @bot.callback_query_handler(func = lambda lang_call: lang_call.data in ["english","russian"])
    def lang_callback(lang_call):
        global users_language
        if lang_call.data=="english":
            users_language = 0
        else:
            users_language = 1
        if users_language==0:
            bot.edit_message_text(chat_id=lang_call.message.chat.id, message_id=lang_call.message.message_id, text="Language was successfully changed.",
                              reply_markup=None)
        else:
            bot.edit_message_text(chat_id=lang_call.message.chat.id, message_id=lang_call.message.message_id,
                                  text="Язык был успешно изменен.",
                                  reply_markup=None)
#get list of places where you can make a coronavirus vaccine
@bot.message_handler(commands=['vaccine'])
def vaccine(message):
    region_keyboard = types.ReplyKeyboardMarkup()
    brest_region_button = types.KeyboardButton(text="Брестская область")
    vitebsk_region_button = types.KeyboardButton(text="Витебская область")
    gomel_region_button = types.KeyboardButton(text="Гомельская область")
    hrodna_region_button = types.KeyboardButton(text="Гродненская область")
    minsk_region_button = types.KeyboardButton(text="Минская область")
    mogilev_region_button = types.KeyboardButton(text="Могилевская область")
    minsk_button = types.KeyboardButton(text="г. Минск")
    region_keyboard.add(brest_region_button, vitebsk_region_button, gomel_region_button)
    region_keyboard.add(hrodna_region_button, minsk_region_button, mogilev_region_button)
    region_keyboard.add(minsk_button)
    if users_language==0:
        bot.send_message(message.chat.id,"This function works only in Belarus yet. Please, choose your region.",reply_markup=region_keyboard)
    else:
        bot.send_message(message.chat.id,"Эта функция работает пока только на территории Беларуси. Пожалуйста, выберите Вашу область.",reply_markup=region_keyboard)
    bot.register_next_step_handler(message,get_vaccine_information)
def get_vaccine_information(message):
    regions_list = ["Брестская область","Витебская область","Гомельская область","Гродненская область","Минская область","Могилевская область","г. Минск"]
    text_1 = message.text
    if text_1 in regions_list:
        if text_1=="г. Минск":
            region_name = "МИНСК"
        else:
            region_name = text_1.upper()
        region_information = str(requests.get('https://1prof.by/news/v-strane/gde-v-minske-i-oblastyah-mozhno-sdelat-privivku-ot-covid-19/').text)
        next_region_dict = {"МИНСК":"МИНСКАЯ ОБЛАСТЬ","МИНСКАЯ ОБЛАСТЬ":"БРЕСТСКАЯ ОБЛАСТЬ","БРЕСТСКАЯ ОБЛАСТЬ":"ВИТЕБСКАЯ ОБЛАСТЬ","ВИТЕБСКАЯ ОБЛАСТЬ":"ГОМЕЛЬСКАЯ ОБЛАСТЬ","ГОМЕЛЬСКАЯ ОБЛАСТЬ":"ГРОДНЕНСКАЯ ОБЛАСТЬ","ГРОДНЕНСКАЯ ОБЛАСТЬ":"МОГИЛЕВСКАЯ ОБЛАСТЬ","МОГИЛЕВСКАЯ ОБЛАСТЬ":'Подготовила Виктория ЯКИМОВА'}#Подготовила Виктория ЯКИМОВА
        text_to_send = region_information[region_information.find(region_name):region_information.find(next_region_dict[region_name])]
        s1 =""
        text_to_send = list(text_to_send)
        i = 0
        while i<len(text_to_send):
            if text_to_send[i]!="<":
                s1+=text_to_send[i]
                i+=1
            else:
                i = text_to_send.index(">")+1
                text_to_send[text_to_send.index(">")]="*"
        part_string = ""
        for i in s1:
            if len(part_string)==2600:
                bot.send_message(message.chat.id,part_string)
                part_string=""
            else:
                part_string+=i
        if len(part_string)!=0:
            bot.send_message(message.chat.id,part_string)
    else:
        if users_language==0:
            bot.send_message(message.chat.id,"Your input is wrong!")
        else:
            bot.send_message(message.chat.id,"Ваш ввод неверен!")
    if users_language==0:
        non_keyboard = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(message.chat.id, "You are welcome! :-)", reply_markup=non_keyboard)
    else:
        non_keyboard = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(message.chat.id, "Не за что! :-)", reply_markup=non_keyboard)
    vaccine_continue_keyboard = types.InlineKeyboardMarkup()
    vaccine_yes = types.InlineKeyboardButton(text="☑️", callback_data="vaccine_yes")
    vaccine_no = types.InlineKeyboardButton(text="❌", callback_data="vaccine_no")
    vaccine_continue_keyboard.add(vaccine_yes, vaccine_no)
    if users_language == 0:
        bot.send_message(message.chat.id, "Do you want to continue?", reply_markup=vaccine_continue_keyboard)
    else:
        bot.send_message(message.chat.id, "Хотите продолжить?", reply_markup=vaccine_continue_keyboard)

    @bot.callback_query_handler(func=lambda vaccine_call: vaccine_call.data in ["vaccine_yes", "vaccine_no"])
    def vaccine_continue_acceptance(vaccine_call):
        if vaccine_call.data == "vaccine_yes":
            bot.edit_message_text(chat_id=vaccine_call.message.chat.id, message_id=vaccine_call.message.message_id,
                                  text="Ok.",
                                  reply_markup=None)
            bot.register_next_step_handler(vaccine_call.message, vaccine)
            if users_language==0:
                bot.send_message(vaccine_call.message.chat.id,"Please send any message.")
            else:
                bot.send_message(vaccine_call.message.chat.id,"Пожалуйста, отправьте любое сообщение.")
        else:
            bot.edit_message_text(chat_id=vaccine_call.message.chat.id, message_id=vaccine_call.message.message_id,
                                  text="Ok.",
                                  reply_markup=None)
#get coronavirus statistics
@bot.message_handler(commands=['stat'])
def statistics(message):
    if users_language==0:
        bot.send_message(message.chat.id,"Send your full country's name in English.")
    else:
        bot.send_message(message.chat.id,"Отправьте полное название Вашей страны на английском.")
    bot.register_next_step_handler(message,choose_country)
def choose_country(message):
    date = str(datetime.date.today())
    country_dict = {"Belarus": "belarus", "Russia": "russia","Usa":"us","India":"india","Brazil":"brazil","Uk":"uk","France":"france",
                    "Turkey":"turkey","Argentina":"argentina","Iran":"iran","Colombia":"colombia","Spain":"spain","Italy":"italy","Indonesia":"indonesia",
                    "Germany":"germany","Mexico":"mexico","Poland":"poland","South africa":"south-africa","Ukraine":"ukraine","Peru":"peru",
                    "Philippines":"philippines","Netherlands":"netherlands","Iraq":"iraq","Malaysia":"malaysia","Czechia":"czechia","Chile":"chile",
                    "Japan":"japan","Bangladesh":"bangladesh","Canada":"canada","Thailand":"thailand","Belgium":"belgium","Sweden":"sweden",
                    "Israel":"israel","Lithuania":"lithuania","Norway":"norway","Latvia":"latvia","Estonia":"estonia","China":"china","Moldova":"moldova",
                    "Finland":"finland","Denmark":"denmark","Romania":"romania","Bulgaria":"bulgaria","Switzerland":"switzerland"}
    country_name = str(message.text).strip().strip("/").capitalize()
    if country_name in country_dict:
        country_information = str(requests.get(f"https://www.worldometers.info/coronavirus/country/{country_dict[country_name]}/").content)
        cases_index = country_information.find('Coronavirus Cases:')
        recovered_index = country_information.find('Recovered:')
        s1 = (country_information[cases_index:recovered_index+100].split("\\n"))
        updates_index = country_information.find("Updates")
        s2 = (country_information[updates_index:]).split("\\n")[2]
        new_lst = []
        s2 = s2.replace("<strong>","$")
        s2 = s2.replace("</strong>","*")
        for i in range(len(s2)):
            if s2[i]=="$":
                s3 = s2[i:s2.index("*")].split()
                new_lst.append(s3[0][1:])
                s2 = s2[:s2.index("*")]+"&"+s2[s2.index("*")+1:]
        new_lst = new_lst[:2]
        for i in range(len(new_lst)):
            if new_lst[i]=="<a":
                new_lst[i]="0"
        if users_language==0:
            bot.send_message(message.chat.id,
                             f"Information on {date}: \nCoronavirus cases: {s1[2][s1[2].index('>') + 1:s1[2].index('/span') - 1].strip()} + {new_lst[0]};\nDeaths: {s1[8][s1[8].index('>') + 1:s1[8].index('/span') - 1].strip()} + {new_lst[1]};\nRecovered: {s1[14][s1[14].index('>') + 1:s1[14].index('/span') - 1].strip()}.")
        else:
            bot.send_message(message.chat.id,
                             f"Информация на {date}: \nСлучаи коронавируса: {s1[2][s1[2].index('>') + 1:s1[2].index('/span') - 1].strip()} + {new_lst[0]};\nСмерти: {s1[8][s1[8].index('>') + 1:s1[8].index('/span') - 1].strip()} + {new_lst[1]};\nВыздоровевшие: {s1[14][s1[14].index('>') + 1:s1[14].index('/span') - 1].strip()}.")
    else:
        similar_dict = {}
        for i in country_dict:
            similar_dict[i] = similar(message.text, i)
        sorted_dict = dict(sorted(similar_dict.items(), key=lambda item: item[1], reverse=True))
        if users_language==0:
            bot.send_message(message.chat.id,f"Your input is wrong or we don't have information about this country. Maybe you meant: \n/{list(sorted_dict.keys())[0]} \n/{list(sorted_dict.keys())[1]} \n/{list(sorted_dict.keys())[2]}")
        else:
            bot.send_message(message.chat.id,f"Ваш ввод неверен либо у нас нет информации об этой стране. Возможно Вы имели в виду: \n/{list(sorted_dict.keys())[0]} \n/{list(sorted_dict.keys())[1]} \n/{list(sorted_dict.keys())[2]}")
    stat_continue_keyboard = types.InlineKeyboardMarkup()
    yes_stat_continue_but=types.InlineKeyboardButton(text="☑️",callback_data="yes_stat")
    no_stat_continue_but = types.InlineKeyboardButton(text="❌",callback_data="no_stat")
    stat_continue_keyboard.add(yes_stat_continue_but,no_stat_continue_but)
    if users_language==0:
        bot.send_message(message.chat.id,"Do you want to continue?",reply_markup=stat_continue_keyboard)
    else:
        bot.send_message(message.chat.id,"Хотите продолжить?", reply_markup=stat_continue_keyboard)

    @bot.callback_query_handler(func=lambda stat_call: stat_call.data in ["yes_stat", "no_stat"])
    def stat_continue_acceptance(stat_call):
        if stat_call.data == "yes_stat":
            if users_language==0:
                bot.send_message(stat_call.message.chat.id,"Send your full country's name on english.")
                bot.register_next_step_handler(stat_call.message,choose_country)
            else:
                bot.send_message(stat_call.message.chat.id, "Отправьте полное название Вашей страны на английском.")
                bot.register_next_step_handler(stat_call.message, choose_country)
        else:
            pass
        bot.edit_message_text(chat_id=stat_call.message.chat.id, message_id=stat_call.message.message_id,
                              text="Ok.",
                              reply_markup=None)
#get my contacts
@bot.message_handler(commands = ['author'])
def author(message):
    global users_language
    if users_language==0:
        bot.send_message(message.chat.id, "If you have any advices or you have any problems write on this email: fedarau@gmail.com.")
        bot.send_message(message.chat.id,"There is author's Telegram contact:")
        bot.send_contact(message.chat.id,'+375336862112','navajo')
    else:
        bot.send_message(message.chat.id,
                         "Если у вас есть какие-либо предложения или проблемы,тогда свяжитесь с автором по этой почте: fedarau@gmail.com.")
        bot.send_message(message.chat.id,"Телеграм контакт автора: ")
        bot.send_contact(message.chat.id, '+375336862112', 'navajo')
#other cases
@bot.message_handler(func  = lambda m: True)
def base(message):
    global users_language
    if users_language==0:
        bot.send_message(message.chat.id,"Your input is wrong.")
    else:
        bot.send_message(message.chat.id,"Ваш ввод неверен.")

bot.polling(none_stop=True)
