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
def set_native_language(language_code):
    global users_language
    users_language_code = language_code
    if users_language_code == "ru":
        users_language = 1
    else:
        users_language = 0
#start command
@bot.message_handler(commands = ['start'])
def start(message):
    global users_language#text depends on users's language. By default it's English
    set_native_language(message.from_user.language_code)
    if users_language == 0:
        bot.send_message(message.chat.id,f"Hello, {message.from_user.first_name}!")
        bot.send_message(message.chat.id,"If you have any troubles use /author to get author's contacts.")
    else:
        bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}!")
        bot.send_message(message.chat.id, "Еcли у Вас возникли какие-либо проблемы, тогда используйте /author, чтобы получить контакты автора.")
@bot.message_handler(commands=['geo'])
def geo(message):
    set_native_language(message.from_user.language_code)
    geo_keyboard=types.ReplyKeyboardMarkup(resize_keyboard=True)
    geo_yes = types.KeyboardButton(text="☑️",request_location=True)
    geo_no = types.KeyboardButton(text="❌")
    geo_keyboard.add(geo_yes,geo_no)
    if users_language==0:
        bot.send_message(message.from_user.id,"Input your geoposition.",reply_markup=geo_keyboard)
    else:
        bot.send_message(message.from_user.id, "Введите Вашу геопозицию.", reply_markup=geo_keyboard)
    bot.register_next_step_handler(message,geo_continue)
def geo_continue(message):
    if message.location!=None:
        from geopy import Nominatim
        global locator
        locator = Nominatim(user_agent="myGeocoder")
        global users_latitude,users_longitude
        users_latitude = message.location.latitude
        users_longitude = message.location.longitude
        users_geo_data = locator.reverse(f"{message.location.latitude}, {message.location.longitude}",language="ru").raw#53.9024716 27.5618225
        users_country_code = users_geo_data['address']['country_code']
        if users_country_code=="by":
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
                bot.send_message(message.chat.id,"Choose your region.",reply_markup=region_keyboard)
            else:
                bot.send_message(message.chat.id, "Выберите Вашу область.", reply_markup=region_keyboard)
            bot.register_next_step_handler(message,geo_continue_1)
        else:
            if users_language==0:
                bot.send_message(message.chat.id,"Sorry, this function works only in Belarus, yet.")
            else:
                bot.send_message(message.chat.id, "Извините, эта функция работает пока только в Беларуси.")
            non_keyboard = types.ReplyKeyboardRemove(selective=False)
            bot.send_message(message.chat.id, "Ok.", reply_markup=non_keyboard)
    else:
        non_keyboard = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(message.chat.id, "Ok.", reply_markup=non_keyboard)
def geo_continue_1(message):
    global locator, users_latitude, users_longitude
    regions_list = ["Брестская область","Витебская область","Гомельская область","Гродненская область","Минская область","Могилевская область","г. Минск"]
    non_keyboard = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, "Ok.", reply_markup=non_keyboard)
    if message.text in regions_list:
        if message.text=="г. Минск":
            pass#смотрим по районам
        else:
            import numpy as np
            places_list = np.array([])
            cities_list = np.array([])
            if message.text=="Гродненская область":
                cities_list = np.array(["Гродно","Большая Берестовица","Волковыск","Вороново, Беларусь","Дятлово","Зельва","Ивье",'Лида, Беларусь',"Радунь","Кореличи","Мосты, Гродненская область, Беларусь","Новогрудок","Островец","Ошмяны","Свислочь","Щучин, Беларусь","Сморгонь","Слоним"])
                places_list = np.array([["Центральная городская поликлиника, Гродно","Городская поликлиника №3, Гродно","Городская поликлиника №4, Гродно","Городская поликлиника №5, Гродно","Городская поликлиника №6, Гродно","Городская поликлиника №7, Гродно"],["Берестовицкая центральная районная больница, Большая Берестовица"],["Центральная районная больница, Волковыск"],["Вороновская центральная районная больница, Вороново"],
                                        ["Дятловская центральная районная больница, Дятлово"],["Зельвенская центральная районная больница, Зельва"],["Ивьевская центральная районная больница,Ивье"],["Лидская центральная районная больница, Лида", "Городская поликлиника №1, Лида"],["Радунь"],
                                        ["Кореличи"],["Центральная районная больница, Мосты, Гродненская область"],["Новогрудская ЦРБ, Новогрудок"],["Островец"],["Ошмянская центральная районная больница, Ошмяны"],["Свислочская Центральная районная больница, Свислочь"],["Щучинская центральная районная больница, Щучин"],["Сморгонская Центральная районная больница, Сморгонь"],["Слонимская центральная районная больница, Слоним"]])
            elif message.text=="Могилевская область":
                cities_list = np.array(["Белыничи","Быхов","Глуск","Горки, Беларусь","Дрибин","Кировск, Беларусь","Климовичи","Кличев, Беларусь","Костюковичи","Краснополье, Беларусь","Кричев","Круглое, Беларусь","Мстиславль","Осиповичи","Славгород, Беларусь","Хоцімск","Чаусы","Чериков","Шклов","Могилев"])
                places_list = np.array([["Белыничская центральная районная больница, Белыничи"],["Быховская центральная районная больница, Быхов"],["Глусская ЦРБ, Глуск"],["Горецкая центральная районная больница, Горки , Беларусь"],["Поликлиника, Дрибин"],["ЦРБ, Кировск, Беларусь"],["Климовическая районная поликлиника, Климовичи"],["Районная больница, Кличев, Беларусь"],["Больница, Костюковичи"],["ЦРБ, Краснополье, Беларусь"]
                                           ,["Кричевская Цетральная Районная Больница, Кричев, Беларусь"],["Круглянская больница, Круглое, Беларусь"],["Мстиславльская центральная районная больница, Мстиславль"],["Осиповичская центральная районная больница, Осиповичи"],["Славгород, Беларусь"],["Хотимская центральная районная больница, Хоцімск"],["Отделение Скорой Медицинской Помощи, Чаусы"],["Чериковская центральная районная больница, Чериков"],
                                        ["""УЗ "Шкловская ЦРБ", Шклов"""],[""]])
            else:
                cities_list = np.array(
                    ["Гродно", "Большая Берестовица", "Волковыск", "Вороново, Беларусь", "Дятлово", "Зельва", "Ивье",
                     'Лида, Беларусь', "Радунь", "Кореличи", "Мосты, Гродненская область, Беларусь", "Новогрудок",
                     "Островец", "Ошмяны", "Свислочь", "Щучин, Беларусь", "Сморгонь", "Слоним"])
                places_list = np.array([["Центральная городская поликлиника, Гродно",
                                         "Городская поликлиника №3, Гродно", "Городская поликлиника №4, Гродно",
                                         "Городская поликлиника №5, Гродно", "Городская поликлиника №6, Гродно",
                                         "Городская поликлиника №7, Гродно"],
                                        ["Берестовицкая центральная районная больница, Большая Берестовица"],
                                        ["Центральная районная больница, Волковыск"],
                                        ["Вороновская центральная районная больница, Вороново"],
                                        ["Дятловская центральная районная больница, Дятлово"],
                                        ["Зельвенская центральная районная больница, Зельва"],
                                        ["Ивьевская центральная районная больница,Ивье"],
                                        ["Лидская центральная районная больница, Лида",
                                         "Городская поликлиника №1, Лида"], ["Радунь"],
                                        ["Кореличи"], ["Центральная районная больница, Мосты, Гродненская область"],
                                        ["Новогрудская ЦРБ, Новогрудок"], ["Островец"],
                                        ["Ошмянская центральная районная больница, Ошмяны"],
                                        ["Свислочская Центральная районная больница, Свислочь"],
                                        ["Щучинская центральная районная больница, Щучин"],
                                        ["Сморгонская Центральная районная больница, Сморгонь"],
                                        ["Слонимская центральная районная больница, Слоним"]])
            cities_ans_dist = 10000.0
            cities_ans_name=2
            if users_language == 0:
                bot.send_message(message.chat.id, f"We are finding closest to you city -- about {len(cities_list)} seconds.")
            else:
                bot.send_message(message.chat.id, f"Мы ищем ближайший к Вам город -- около {len(cities_list)} секунд.")
            users_data = (users_latitude, users_longitude)
            for i in np.arange(0,len(cities_list),1):
                users_city = cities_list[i]
                chosen_city_data = locator.geocode(users_city)
                users_city_latitude = chosen_city_data.latitude
                users_city_longitude = chosen_city_data.longitude
                city_data = (users_city_latitude,users_city_longitude)
                from geopy import distance
                city_distance_data = distance.distance(city_data, users_data)
                if city_distance_data<cities_ans_dist:
                    cities_ans_name=i
                    cities_ans_dist = city_distance_data
            places_list = places_list[cities_ans_name]
            ans_dist = 10 ** 5.0
            ans_latitude = 0.0
            ans_longitude = 0.0
            if users_language==0:
                bot.send_message(message.chat.id, f"Please wait about {len(places_list)} seconds.")
            else:
                bot.send_message(message.chat.id,f"Подождите около {len(places_list)} секунд.")
            point_ans_name = ""
            for i in np.arange(0, len(places_list), 1):
                chosen_place = places_list[i]
                chosen_place_data = locator.geocode(chosen_place)
                place_latitude = chosen_place_data.latitude
                place_longitude = chosen_place_data.longitude
                place_data = (place_latitude, place_longitude)
                from geopy import distance
                distance_data = distance.distance(place_data, users_data)
                if distance_data < ans_dist:
                    ans_latitude = place_latitude
                    ans_longitude = place_longitude
                    ans_dist = distance_data
                    point_ans_name = chosen_place
            bot.send_location(message.chat.id, ans_latitude, ans_longitude)
            if places_list==['Радунь']:
                bot.send_message(message.chat.id,"Радунская поликлиника, Радунь")
            elif places_list==['Кореличи']:
                bot.send_message(message.chat.id, "Кореличская ЦРБ, Кореличи")
            elif places_list==["Островец"]:
                bot.send_message(message.chat.id,"Островецкая ЦРКБ, Островец")
            elif places_list==['Кричевская Цетральная Районная Больница, Кричев, Беларусь']:
                bot.send_message(message.chat.id,"Кричевская ЦРБ, Кричев")
            elif places_list == ["Славгород, Беларусь"]:
                bot.send_message(message.chat.id,"Славгородская ЦРБ, Беларусь")
            elif places_list == ["Хотимская центральная районная больница, Хоцімск"]:
                bot.send_message(message.chat.id,"Хотимская центральная районная больница, Хотимск")
            elif places_list == ["Отделение Скорой Медицинской Помощи, Чаусы"]:
                bot.send_message(message.chat.id,"Чаусская ЦРБ, Чаусы")
            else:
                bot.send_message(message.chat.id, point_ans_name)
    else:
        if users_language==0:
            bot.send_message(message.chat.id,"Your input is wrong.")
        else:
            bot.send_message(message.chat.id,"Ваш ввод неверен.")
#get list of places where you can make a coronavirus vaccine
@bot.message_handler(commands=['vaccine'])
def vaccine(message):
    set_native_language(message.from_user.language_code)
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
    set_native_language(message.from_user.language_code)
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
                bot.send_message(stat_call.message.chat.id,"Send your full country's name in English.")
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
    set_native_language(message.from_user.language_code)
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
    set_native_language(message.from_user.language_code)
    global users_language
    if users_language==0:
        bot.send_message(message.chat.id,"Your input is wrong.")
    else:
        bot.send_message(message.chat.id,"Ваш ввод неверен.")
bot.polling(none_stop=True)
