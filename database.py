import sqlite3
import requests
global conn
global cursor
import vk_api
from random import randint
token='e42eedf69d3dd1946053e7c6feb66add3d58ec37bf209da76cb1315e9b3c849e0179aea1e334188895593'

atrib={
        "имя":"name","раса":"race","сила":"strength","ловкость":"dexterity","телосложение":"constitution",
        "интеллект":"intelligence","харизма":"charisma","ментальная_устойчивость":"mental_stability",
        "физическое_здоровье":"f_life","ментальное_здоровье":"m_life","магия":"magic","рукопашный_бой":"hand_combat",
        "холодное_оружие":"cold_steel","огнестрельное_оружие":"firearm","маскировка":"disguise","обнаружение":"detection",
        "техника_и_электроника":"equipment&electronic","компьютеры_и_программирование":"programming",
        "вождение":"driving","знание_языков":"languages","природоведение":"natural_study","медицина":"medicine",
        "ловкость_рук":"sleight_of_hand","очки_особенностей":"points_features","особенности":"features","инвентарь":"items"
        }

#получение всех имён
def AllName():
    name=dict()#оздаём словарь который будем возвращать
    cursor.execute('SELECT Name FROM profil')#переносим курсор на колонку username в базе данных
    username=cursor.fetchall()# заносим список из кортежей в переменную
    cursor.execute('SELECT Number FROM profil')
    Id=cursor.fetchall()
    for i in range(len(Id)):
        name[username[i][0]]=Id[i][0] #заполняем словарь из имён пользователей и их номере в базе данных
    return name



# Создание нового персонажа
def EntryDataFull(a,event):
    print(a,len(a))
    All=AllName()
    if a[0] in All:
        return "Тёзкам не рады"
    cursor.execute("INSERT INTO profil VALUES (null,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,0,?)",a)# делаем sqlite запрос на создание новой строки в таблице
    conn.commit()#сохранение изменений
    return "Персонаж "+a[0]+" создан"
# Вывод всей информации о персонаже
def AllInfo(post_id):
    skills={
        16:"Рукопашный бой", 17:"Холодное оружие", 18:"Огнестрельное оружие", 19:"Маскировка", 20:"Обнаружение",
        21:"Техника и электроника", 22:"Компьютеры и программирование",23:"вождение",24:"Знание языков",25:"природоведение",
        26:"медицина",27:"ловкость рук"}
    All=AllName()
    post_id=All[post_id]
    cursor.execute("SELECT * FROM profil Where Number="+str(post_id))
    info=list(cursor.fetchall()[0])
    for i in range(0,len(info)):
        if info[i]==None:
            info[i]="Н/Д"
    answer=str()
    answer="Имя: "+info[1]+"\n"
    answer+="Раса: "+info[2].replace('_',' ')+"\n"
    answer+="Характеристики\n"
    answer+="\U0001F4AA Сила: "+str(info[3])+"\n"
    answer+="\U0001F938 Ловкость: "+str(info[4])+"\n"
    answer+="\U0001F3CB Телосложение: "+str(info[5])+"\n"
    answer+="\U0001F9E0 Интеллект: "+str(info[6])+"\n"
    answer+="\U0001F57A Харизма: "+str(info[7])+"\n"
    answer+="\U0001F9D8 Ментальная защита: "+str(info[8])+"\n"
    answer+="Физическое здоровье: "
    for i in str(info[11]):
        answer+=i+"\u20E3"
    answer+=" из "+str(info[9])+"\n"
    answer+="Ментальная здоровье: "
    for i in str(info[12]):
        answer+=i+"\u20E3"
    answer+=" из "+str(info[10])+"\n"
    if "Пионер" in info[29]:
        answer+="Режим пионера: "
    elif info[2]=="вампир":
        answer+="Обращение: "
    else:
        answer+="Магия: "
    for j in range(1,info[13]+1):
        if j<=info[14]:
            answer+="\U00002B1B"
        else:
            answer+="\U000025FB"
    answer+=" "+str(info[14])+"/"+str(info[13])+"\n"
    answer+="Навыки\n"
    for i in range(16,28):
        answer+=skills[i]+" "
        for j in range(1,5):
            if j<=info[i]:
                answer+="\U00002B1B"
            else:
                answer+="\U000025FB"
        answer+=" "+str(info[i])+"\n"
    answer+="Очки особенностей: "+str(info[28])+"\n"
    answer+="Особенности: "+info[29].replace(" ",", ").replace("_"," ")+"\n"
    answer+="Деньги: "+str(info[30])+" cr\n"
    answer+="Инвентарь: "+info[31].replace(" ",", ").replace("_"," ")+"\n"
    return answer

def bonusFate(Name,Character):
    post_id=AllName()
    post_id=post_id[Name]
    cell=""
    bonus=0
    for i in Character:
        cell+=atrib[i]+","
    cell=cell[:-1]
    cursor.execute("SELECT "+cell+" FROM profil where Number="+str(post_id))
    chart=list(cursor.fetchall()[0])
    for i in chart:
        if i>4:
            i=int((i-10)/2)
        bonus+=i
    return bonus

def HowValue(post_id,atrib):
    cursor.execute("SELECT "+atrib+" FROM profil where Number="+str(post_id))
    atrib=list(cursor.fetchall()[0])
    return atrib

def UpdateValue(post_id,update,post_id1):

    conn.execute("UPDATE profil SET "+update+" WHERE Number="+str(post_id))#изменение значений таблицы    
    conn.commit()
    return "Данные обновлены\n"


def TransformValue(post_id,atrib):
    cursor.execute("SELECT "+atrib+" FROM profil where Number="+str(post_id))
    atrib=list(cursor.fetchall()[0])
    return atrib

def CombatMode(text):
    All=AllName()
    post_id=All[text[1]]
    update=""
    cursor.execute("SELECT combat_mode,race,features,dexterity,constitution FROM profil where Number="+str(post_id))
    mode=list(cursor.fetchall()[0])
    answer=""
    if mode[0]:
        if mode[1]=="вампир":
            update+="constitution="+str(mode[4]-1)+","
        if "Пионер_А" in mode[2]:
            update+="constitution="+str(mode[4]-1)+","
            update+="dexterity="+str(mode[3]-1)+","
        update+="combat_mode=0"
        answer="Деактивация боевого режима"
    else:
        if mode[1]=="вампир":
            update+="constitution="+str(mode[4]+1)+","
        elif "Пионер_А" in mode[2]:
            update+="constitution="+str(mode[4]+1)+","
            update+="dexterity="+str(mode[4]+1)+","
        else:
            return "У тебя нет боевого режима, немощный"
        update+="combat_mode=1"
        answer="Активация боевого режима"
    conn.execute("UPDATE profil SET "+update+" WHERE Number="+str(post_id))
    conn.commit()
    return answer

def DrinkBlood(text):
    All=AllName()
    post_id=All[text[1]]

    update=""
    cursor.execute("SELECT race,max_f_life, madness FROM profil where Number="+str(post_id))
    madness=list(cursor.fetchall()[0])
    if madness[0]=="вампир":
        update="f_life="+"".join(list(str(i) for i in range(1,madness[1]+1)))+","
        madness[2]+=randint(1,4)
        if madness[2]>=:
        	conn.execute("UPDATE profil SET "+update+"magic=7, madness="+str(0)+" WHERE Number="+str(post_id))
        	return "Ты обезумел. Твоё тело во власти мастера"
        conn.execute("UPDATE profil SET "+update+"magic=7, madness="+str(madness[2])+" WHERE Number="+str(post_id))
        conn.commit()
        return "Магма течёт в твоих венах. Вкусная кровинушка? Ты полон сил"
    else:
        return "Ну пьёт и пьёт, чего бухтеть-то?"

def HealValue(text):
    All=AllName()
    post_id=All[text[1]]
    flag=0
    if text[3]=="ментально":
        cursor.execute("SELECT max_m_life FROM profil where Number="+str(post_id))
        life=cursor.fetchall()[0][0]
        if life>=int(text[4]):
            flag="".join(list(str(i) for i in range(1,int(text[4])+1)))
        else:
            flag="".join(list(str(i) for i in range(1,flag+1)))
        conn.execute("UPDATE profil SET m_life="+flag+" WHERE Number="+str(post_id))
        conn.commit()
        return "оставшиеся ячейки "+flag

    elif text[3]=="физически":
        cursor.execute("SELECT max_f_life FROM profil where Number="+str(post_id))
        life=cursor.fetchall()[0][0]
        if life>=int(text[4]):
            flag="".join(list(str(i) for i in range(1,int(text[4])+1)))
        else:
            flag="".join(list(str(i) for i in range(1,life+1)))

        conn.execute("UPDATE profil SET f_life="+flag+" WHERE Number="+str(post_id))
        conn.commit()
        return "оставшиеся ячейки "+flag
    else:
        return "Похоже не лечишься"

def WoundValue(text):
    All=AllName()
    post_id=All[text[1]]
    flag=0
    if text[3]=="ментально":
        cursor.execute("SELECT m_life FROM profil where Number="+str(post_id))
        life=cursor.fetchall()[0][0]
        for i in str(life):
            if i>=text[4]:
                life=str(life).replace(i,"")
                flag=1
                break
        if not flag:
            return "Похоже ты отключился"
        if life=="":
            life="0"
        conn.execute("UPDATE profil SET m_life="+life+" WHERE Number="+str(post_id))
        conn.commit()
        return "оставшиеся ячейки "+life

    elif text[3]=="физически":
        cursor.execute("SELECT f_life FROM profil where Number="+str(post_id))
        life=cursor.fetchall()[0][0]
        for i in str(life):
            if i>=text[4]:
                life=str(life).replace(i,"")
                flag=1
                break
        if not flag:
            return "Похоже ты отключился"
        if life=="":
            life="0"
        conn.execute("UPDATE profil SET f_life="+life+" WHERE Number="+str(post_id))
        conn.commit()
        return "оставшиеся ячейки "+life
    else:
        return "Похоже не ранен"

def DeleteValue(post_id,atrib,cell):
    if atrib:
        cursor.execute("SELECT "+cell+" FROM profil where Number="+str(post_id))
        atrib1=cursor.fetchall()[0][0]
        if atrib1==None:
            return"Н/Д"
        else:
            atrib1=atrib1.split(" ")
        for i in atrib:
            try:
                atrib1.remove(i)
            except ValueError:
                continue
        conn.execute("UPDATE profil SET "+cell+" ='"+' '.join(atrib1)+"'WHERE Number="+str(post_id))#изменение значений таблицы    
        conn.commit()
        return atrib1
    else:
        conn.execute("UPDATE profil SET "+cell+"=NULL WHERE Number="+str(post_id))#изменение значений таблицы
        conn.commit()
        return "Все данные ячейки удалены"


def NewValue(value,post_id,cell):
    cursor.execute("SELECT "+cell+" FROM profil where Number="+str(post_id))
    atrib= cursor.fetchall()[0][0]
    if atrib==None:
        conn.execute("UPDATE profil SET "+cell+" ='"+str(value)+"'WHERE Number="+str(post_id))#изменение значений таблицы
        conn.commit()
        return value.split(' ')
    else:
        atrib+=" "+str(value)
        conn.execute("UPDATE profil SET "+cell+" ='"+str(atrib)+"'WHERE Number="+str(post_id))#изменение значений таблицы
        conn.commit()
    return atrib.split(' ')

# работа с таблицей мастеров
# добавление чата в список рабочих
def NewDialogs(vk,event):
    print(event.object.peer_id)
    userchat=vk.messages.getConversationMembers(peer_id=event.object.peer_id)# запрос на информацию о всех пользователях беседы
    master=0
    for i in userchat['items']:
        if 'is_owner' in i:
            master=i['member_id']
    info=[event.object.peer_id,int(master)]
    cursor.execute('INSERT INTO chat VALUES (?,?)',info)# делаем sqlite запрос на создание новой строки в таблице
    conn.commit()#сохранение изменений
    return "Добавили"
# ищем мастера беседы
def HowIsBoss(post_id):
    cursor.execute("SELECT chat_id FROM profil where Number="+str(post_id))
    chat_id=cursor.fetchall()[0][0]
    cursor.execute("SELECT master_id FROM chat where chat_id="+str(chat_id))
    return cursor.fetchall()[0][0]

def BigBoss(persona,master):
    cursor.execute("SELECT chat_id FROM chat where master_id="+str(master))
    chat=cursor.fetchall()
    cursor.execute("SELECT chat_id FROM profil where Number="+str(persona))
    userchat=cursor.fetchall()[0][0]
    for i in chat:
        if userchat in i:
            return True
    return False 
# chat_id игрока
def TrueDialog(post_id):
    cursor.execute("SELECT chat_id FROM profil where Number="+str(post_id))
    userchat=cursor.fetchall()[0][0]
    return userchat
# определяем, является человек мастером
def MasterChat(user_id):
    cursor.execute("SELECT master_id FROM chat where master_id="+str(user_id))
    master=cursor.fetchall()
    if master:
        return master[0][0]
    else:
        return"Владыка не одобрит твоих действий"
# мастер определённого чата
def Master(event):
    print(event.peer_id)
    cursor.execute("SELECT master_id FROM chat where chat_id="+str(event.peer_id))
    print(cursor.fetchall())
    return cursor.fetchall()[0][0]
# назначение нового мастера
def NewMaster(newmaster,vk,event,name):
    oldmaster=Master(key)
    user_id=event.object.from_id
    if int(oldmaster)==int(user_id):
        conn.execute("UPDATE chat set master_id="+str(newmaster)+" Where chat_id="+str(key))
        conn.commit()
        p=vk.messages.getConversationsById(peer_id=event.object.peer_id)
        return "@id"+str(newmaster)+" ("+name+"), Новый владыка "+p["items"][0]['chat_settings']['title']+"! Поприветсвуем же его!"

#Работа с деньгами
# изменение баланса у пользователя
def NewMoney(money,post_id):
    conn.execute("UPDATE profil set Money = "+str(money)+" where Number="+str(post_id))#изменение значений таблицы
    conn.commit()
    return "Новый баланс: "+str(money)+" Денежных единиц"
# запрос баланса у пользователя 
def HowManyMoney(post_id):
    cursor.execute("SELECT Money FROM profil where Number="+str(post_id))
    money = cursor.fetchall()[0][0]
    return money

conn = sqlite3.connect('profil.sqlite3')#подключение к базе данных
cursor = conn.cursor()# создание курсора
conn.commit()



#интересный код
#def switch(case):
#    return{
#            case==50: 4,
#            28<case<50: 3,
#            13<case<29: 2,
#             3<case<14: 1,
#            case<3: 0,
#    }[True]