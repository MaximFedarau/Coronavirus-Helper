import discord
import requests
import datetime
from difflib import SequenceMatcher
from discord.ext import commands
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
bot = commands.Bot(command_prefix='!')
users_language = 0
language_list=["English","Русский"]
bot.remove_command("help")
@bot.group(invoke_without_command=True)
async def help(ctx):
    if users_language==0:
        em = discord.Embed(title="Commands",description="")
        em.add_field(name="!help (Requires: None)",value="Get the list of commands.")
        em.add_field(name="!language (Requires: language)",value="Set your native language.")
        em.add_field(name="!stat (Requires: name of country in English)", value="Get statistics of coronavirus cases around the world.")
        em.add_field(name="!author (Requires: None)",value = "Get author's contacts.")
        em.add_field(name="!vaccine (Requires: name of region) !!!WORKS ONLY IN BELARUS!!!",value="Get the list of places in your region, where you can made a vaccine.")
    else:
        em = discord.Embed(title="Команды", description="")
        em.add_field(name="!help (Требуется: Ничего)", value="Получить список команд.")
        em.add_field(name="!language (Требуется: язык)", value="Выбрать свой родной язык.")
        em.add_field(name="!stat (Требуется: название страны на английском)",
                     value="Получить статистику по коронавирусу по всему миру.")
        em.add_field(name="!author (Требуется: Ничего)", value="Получить контакты автора.")
        em.add_field(name="!vaccine (Требуется: название области) !!!РАБОТАЕТ ТОЛЬКО В БЕЛАРУСИ!!!",value="Получить список мест в вашей области, где Вы можете сделать вакцину.")
    await ctx.send(embed=em)
@bot.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.MissingRequiredArgument):
        if users_language==0:
            await ctx.send("Your input is wrong! You missed some argument!")
        else:
            await ctx.send("Ваш ввод неверен! Вы пропустили какой-то аргумент!")
@bot.command()
async def language(ctx, *args):
    global users_language
    language_options = ""
    for i in language_list:
        language_options+="!language"+" "+i+"\n"
    if args==():
        if users_language==0:
            await ctx.send("There is a list of available languages:")
        else:
            await ctx.send("Вот список доступных языков:")
        await ctx.send(language_options)
    chosen_language = args[0].strip().capitalize()
    if chosen_language in language_list:
        if chosen_language=="English":
            await ctx.send("Your language was successfully changed!")
            users_language=0
        else:
            await ctx.send("Ваш язык был успешно изменен!")
            users_language=1
    else:
        if users_language==0:
            await ctx.send("Your input is wrong! There is a list of available languages:")
            await ctx.send(language_options)
        else:
            await ctx.send("Ваш ввод неверен! Вот список доступных языков:")
            await ctx.send(language_options)
@bot.command()
async def stat(ctx,*args):
    if args==():
        if users_language==0:
            await ctx.send("Your input is wrong. Please, choose country.")
        else:
            await ctx.send("Ваш ввод неверен. Пожалуйста, выберите страну на английском языке.")
    else:
        country_dict = {"Belarus": "belarus", "Russia": "russia", "Usa": "us", "India": "india", "Brazil": "brazil",
                        "Uk": "uk", "France": "france",
                        "Turkey": "turkey", "Argentina": "argentina", "Iran": "iran", "Colombia": "colombia",
                        "Spain": "spain", "Italy": "italy", "Indonesia": "indonesia",
                        "Germany": "germany", "Mexico": "mexico", "Poland": "poland", "South africa": "south-africa",
                        "Ukraine": "ukraine", "Peru": "peru",
                        "Philippines": "philippines", "Netherlands": "netherlands", "Iraq": "iraq",
                        "Malaysia": "malaysia", "Czechia": "czechia", "Chile": "chile",
                        "Japan": "japan", "Bangladesh": "bangladesh", "Canada": "canada", "Thailand": "thailand",
                        "Belgium": "belgium", "Sweden": "sweden",
                        "Israel": "israel", "Lithuania": "lithuania", "Norway": "norway", "Latvia": "latvia",
                        "Estonia": "estonia", "China": "china", "Moldova": "moldova",
                        "Finland": "finland", "Denmark": "denmark", "Romania": "romania", "Bulgaria": "bulgaria",
                        "Switzerland": "switzerland"}
        date = str(datetime.date.today())
        country_name = str(args[0]).strip().strip("/").capitalize()
        if country_name in country_dict:
            country_information = str(requests.get(
                f"https://www.worldometers.info/coronavirus/country/{country_dict[country_name]}/").content)
            cases_index = country_information.find('Coronavirus Cases:')
            recovered_index = country_information.find('Recovered:')
            s1 = (country_information[cases_index:recovered_index + 100].split("\\n"))
            updates_index = country_information.find("Updates")
            s2 = (country_information[updates_index:]).split("\\n")[2]
            new_lst = []
            s2 = s2.replace("<strong>", "$")
            s2 = s2.replace("</strong>", "*")
            for i in range(len(s2)):
                if s2[i] == "$":
                    s3 = s2[i:s2.index("*")].split()
                    new_lst.append(s3[0][1:])
                    s2 = s2[:s2.index("*")] + "&" + s2[s2.index("*") + 1:]
            new_lst = new_lst[:2]
            for i in range(len(new_lst)):
                if new_lst[i] == "<a":
                    new_lst[i] = "0"
            if users_language==0:
                await ctx.send(f"Information on {date}: \nCoronavirus cases: {s1[2][s1[2].index('>') + 1:s1[2].index('/span') - 1].strip()} + {new_lst[0]};\nDeaths: {s1[8][s1[8].index('>') + 1:s1[8].index('/span') - 1].strip()} + {new_lst[1]};\nRecovered: {s1[14][s1[14].index('>') + 1:s1[14].index('/span') - 1].strip()}.")
            else:
                await ctx.send(f"Информация на {date}: \nСлучаи коронавируса: {s1[2][s1[2].index('>') + 1:s1[2].index('/span') - 1].strip()} + {new_lst[0]};\nСмерти: {s1[8][s1[8].index('>') + 1:s1[8].index('/span') - 1].strip()} + {new_lst[1]};\nВыздоровевшие: {s1[14][s1[14].index('>') + 1:s1[14].index('/span') - 1].strip()}.")
        else:
            similar_dict = {}
            for i in country_dict:
                similar_dict[i] = similar(args[0], i)
            sorted_dict = dict(sorted(similar_dict.items(), key=lambda item: item[1], reverse=True))
            if users_language==0:
                await ctx.send(f"Your input is wrong or we don't have information about this country. Maybe you meant: \n!stat {list(sorted_dict.keys())[0]} \n!stat {list(sorted_dict.keys())[1]} \n!stat {list(sorted_dict.keys())[2]}")
            else:
                await ctx.send(f"Ваш ввод неверен либо у нас нет информации об этой стране. Возможно Вы имели в виду: \n!stat {list(sorted_dict.keys())[0]} \n!stat {list(sorted_dict.keys())[1]} \n!stat {list(sorted_dict.keys())[2]}")
@bot.command()
async def author(ctx):
    if users_language==0:
        await ctx.send("If you have any advices or you have any problems write on this email: fedarau@gmail.com.")
        await ctx.send("Contacts on Discord: navajo#8621")
    else:
        await ctx.send("Если у вас есть какие-либо предложения или проблемы,тогда свяжитесь с автором по этой почте: fedarau@gmail.com.")
        await ctx.send("Котнтакты в Discord: navajo#8621")
@bot.command()
async def vaccine(ctx, *args):
    if args==() or len(args)!=2:
        if users_language==0:
            await ctx.send("Your input is wrong!")
            await ctx.send("We only have: \n!vaccine Бресткая область \n!vaccine Витебская область \n!vaccine Гомельская область \n!vaccine Гродненская область \n!vaccine Минская область \n!vaccine Могилевская область \n!vaccine г. Минск")
        else:
            await ctx.send("Ваш ввод неверен!")
            await ctx.send(
                "У нас только есть: \n!vaccine Бресткая область \n!vaccine Витебская область \n!vaccine Гомельская область \n!vaccine Гродненская область \n!vaccine Минская область \n!vaccine Могилевская область \n!vaccine г. Минск")
    else:
        regions_list = ["Брестская область", "Витебская область", "Гомельская область", "Гродненская область",
                        "Минская область", "Могилевская область", "г. Минск"]
        text_1 = args[0]+" "+args[1]
        if text_1 in regions_list:
            if text_1 == "г. Минск":
                region_name = "МИНСК"
            else:
                region_name = text_1.upper()
            region_information = str(requests.get('https://1prof.by/news/v-strane/gde-v-minske-i-oblastyah-mozhno-sdelat-privivku-ot-covid-19/').text)
            next_region_dict = {"МИНСК": "МИНСКАЯ ОБЛАСТЬ", "МИНСКАЯ ОБЛАСТЬ": "БРЕСТСКАЯ ОБЛАСТЬ",
                                "БРЕСТСКАЯ ОБЛАСТЬ": "ВИТЕБСКАЯ ОБЛАСТЬ", "ВИТЕБСКАЯ ОБЛАСТЬ": "ГОМЕЛЬСКАЯ ОБЛАСТЬ",
                                "ГОМЕЛЬСКАЯ ОБЛАСТЬ": "ГРОДНЕНСКАЯ ОБЛАСТЬ",
                                "ГРОДНЕНСКАЯ ОБЛАСТЬ": "МОГИЛЕВСКАЯ ОБЛАСТЬ",
                                "МОГИЛЕВСКАЯ ОБЛАСТЬ": 'Подготовила Виктория ЯКИМОВА'}
            text_to_send = region_information[
                           region_information.find(region_name):region_information.find(next_region_dict[region_name])]
            s1 = ""
            text_to_send = list(text_to_send)
            i = 0
            while i < len(text_to_send):
                if text_to_send[i] != "<":
                    s1 += text_to_send[i]
                    i += 1
                else:
                    i = text_to_send.index(">") + 1
                    text_to_send[text_to_send.index(">")] = "*"
            part_string = ""
            for i in s1:
                if len(part_string) == 1000:
                    await ctx.send(part_string)
                    part_string = ""
                else:
                    part_string += i
            if len(part_string) != 0:
                await ctx.send(part_string)
        else:
            if users_language==0:
                await ctx.send("Your input is wrong!")
                await ctx.send(
                    "We only have: \n!vaccine Бресткая область \n!vaccine Витебская область \n!vaccine Гомельская область \n!vaccine Гродненская область \n!vaccine Минская область \n!vaccine Могилевская область \n!vaccine г. Минск")
            else:
                await ctx.send("Ваш ввод неверен!")
                await ctx.send(
                    "У нас только есть: \n!vaccine Бресткая область \n!vaccine Витебская область \n!vaccine Гомельская область \n!vaccine Гродненская область \n!vaccine Минская область \n!vaccine Могилевская область \n!vaccine г. Минск")
bot.run(TOKEN)
