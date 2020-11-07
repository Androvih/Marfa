import random
import database
import blackjack
import requests
import vk_api
import send

AllName=database.AllName()# берём всё id участников баззы данных в виде словаря
atrib={
        "имя":"name","раса":"race","сила":"strength","ловкость":"dexterity","телосложение":"constitution",
        "интеллект":"intelligence","харизма":"charisma","ментальная_устойчивость":"mental_stability",
        "физическое_здоровье":"f_life","ментальное_здоровье":"m_life","магия":"magic","рукопашный_бой":"hand_combat",
        "холодное_оружие":"cold_steel","огнестрельное_оружие":"firearm","маскировка":"disguise","обнаружение":"detection",
        "техника_и_электроника":"equipment&electronic","компьютеры_и_программирование":"programming",
        "вождение":"driving","знание_языков":"languages","природоведение":"natural_study","медицина":"medicine",
        "ловкость_рук":"sleight_of_hand","очки_особенностей":"points_features","особенности":"features","инвентарь":"items"
        }
# список игроков
def players(vk,event):
    play=""
    i=0
    users=vk.messages.getConversationMembers(peer_id=event.object.peer_id)
    print(users)
    for profil in ( users['profiles']):
        play+=str(profil["first_name"])+" "+str(profil["last_name"])+": "+str(i)+" "# циклично присваиваем каждому человеку псевдоid
        i+=1
    return play
       
def NewMaster(text,vk,event):
    users=vk.messages.getConversationMembers(peer_id=event.object.peer_id)# запрос на информацию о всех пользователях беседы
    for profil in ( users['profiles']):
        if text[3]==profil["last_name"] and text[4]==profil["first_name"]:# создание новой игры
            answer=database.NewMaster(profil["id"],vk,event,profil["first_name"]+" "+profil["last_name"])
            break
    else:
    	answer="Приёмник Владыки не найден"
    return answer

# начало игры в блекджек
#def NewGame(text,key):
 #   player=[]
  #  for i in range(3,len(text)):
   #     if text[i]=="крупье":
    #        break# заполнять список пока не встретим слово крупье
     #   player.append(text[i])
#    diller=text[-1]
 #   blackjack.NewGame(player,key,diller)


 #распределение бонусов здоровья
def switch(case):
    return{
            ((case-10)/2)<2: 0,
            2<=((case-10)/2)<4: 1,
            ((case-10)/2)>=4: 2,
    }[True]

# создание нового пользователя в банковской системе    
def NewUser(event):
    global AllName
    dossier=[]#досье персонажа
    tmp=0
    tmpFI=""
    for i in event.text.split("\n")[1:]:# разбираем текст отправленный через \т
        tmp=i.split(" ")
        if tmp[-1]=='':# убираем точку если кто-то поставил её в конце
            tmp=tmp[:-1]
        if tmp[0]=="рукопашный_бой": #добавление полей здоровья магии и безумия
            for i in range(1,8):
                dossier.append("")
        if tmp[-1].isdigit():
            dossier.append(int(tmp[-1]))
        else:
            if tmp[0] in ["особенности", "инвентарь","раса"]:
                if tmp[0]=="особенности":
                    dossier.append(5)
                tmpFI=""
                for i in tmp[1:]:
                    tmpFI=tmpFI+i+" "
                tmp[-1]=tmpFI[:-1]
            dossier.append(tmp[-1])
    print(dossier)
    dossier[8]=2+switch(dossier[4])
    if dossier[1]=="орк":
        dossier[8]=dossier[8]+1
    dossier[10]=int("".join(list(str(i) for i in range(1,dossier[8]+1))))
    dossier[9]=2+switch(dossier[7])
    dossier[11]=int("".join(list(str(i) for i in range(1,dossier[9]+1))))
    if dossier[1]=="вампир":
        dossier[12]=7
        dossier[13]=7
        dossier[14]=0
    elif "Пионер А" in dossier[28].replace('_',' '):
        dossier[12]=5+int((dossier[4]-10)/2)
        dossier[13]=dossier[12]
    else:
        dossier[12]=5+int((dossier[5]-10)/2)
        if dossier[1]=="квирч":
            dossier[12]=dossier[12]+2
        if dossier[1].replace('_',' ') in ["нёрд","равнинный эльф"]:
            dossier[12]=dossier[12]+1
        dossier[13]=dossier[12]
    dossier.append(int(event.peer_id))
    answer=database.EntryDataFull(dossier,event)#и отправить её в следующую функцию
    AllName=database.AllName()# перезаполнение переменной
    return answer

# запрос на баланс
def HowManyMoney(text):
    try:
        post_id=AllName[text[1]]#получаем номер пользователя по имени
        money=database.HowManyMoney(post_id)#записываем значение баланса в переменную
        return "Баланс "+text[1]+" составляет: "+str(money)+"денежных единиц"
    except KeyError:
        return  "\U0001F632"#если нет запрашевоемого имени обрабатываем ошибку

def Transformswitch(old, new):
    return{
            (old>=4 and new>=2) or (old<2 and new<2) or (2<=old<4 and 2<=new<4): 0,
            (old<2 and 2<=new<4) or(2<=old<4 and new>=4): 1,
            old<2 and new>=4: 2,
    }[True]
def TransformValue(text,event):
    post_id=AllName[text[1]]
    a=atrib[text[3].lower()]+", race,max_f_life,f_life,max_m_life, m_life,max_magic,magic,features"
    Value=database.HowValue(post_id,a)
    newValue=0
    if text[4][0]=="+" or text[4][0]=="-":
        newValue+=Value[0]+int(text[4])
    else:
        return "\U0001F632"
    update=""
    if newValue<0:
        newValue=0
    Trans=Transformswitch(int((Value[0]-10)/2),int((newValue-10)/2))
    life=""
    if text[3]=="телосложение":
        life=Value[3]
        update+="max_f_life="+str(Value[2]+Trans)+", "
        if Trans>0:
            for i in range(Value[2]+1,Value[2]+Trans+1):
                life=str(life)+str(i)
            update+="f_life="+life+", "
        if "Пионер_А" in Value[8]:
            if Value[6]<5+int((newValue-10)/2):
                update+="max_magic="+str(5+int((newValue-10)/2))+", "
                update+="magic="+str(Value[7]+(5+int((newValue-10)/2)-Value[6]))+", "
    if text[3]=="ментальная_устойчивость":
        life=Value[5]
        update+="max_m_life="+str(Value[2]+Trans)+", "
        if Trans>0:
            for i in range(Value[2]+1,Value[2]+Trans+1):
                life=str(life)+str(i)
            update+="m_life="+life+", "
    if text[3]=="интеллект":
        life=5+int((newValue-10)/2)
        if Value[1]=="квирч":
            life+=2
        if Value[1].replace('_',' ') in ["нёрд","равнинный эльф"]:
            life+=1
        if "Пионер_А" not in Value[8] and Value[1]!="вампир":
            if Value[6]<life:
                update+="max_magic="+str(life)+", "
                update+="magic="+str(Value[7]+(life-Value[6]))+", "
    update+=atrib[text[3].lower()]+"="+str(newValue)
    answer=database.UpdateValue(post_id,update,text[1])
    return answer




def DeleteValue(text,event):
    try:
        post_id=AllName[text[1]]
        atributs=text[4:]
        if text[3] not in ["инвентарь", "особенности"]:
            return "не могу"
        a=atrib[text[3].lower()]
        k=database.DeleteValue(post_id,atributs,a)
    except KeyError:
        return  "\U0001F632"
    if type(k)==list:
        for i in range(0,len(k)):
            k[i]=k[i].replace('_',' ')
        return "В ячейке хранятся: "+', '.join(k)
    else:
        return k
def NewValue(text,event):  
    try:
        post_id=AllName[text[1]]
        atributs=" ".join(text[4:])
        if text[3] not in ["инвентарь", "особенности"]:
            return "не могу"
        a=atrib[text[3].lower()]
        k=database.NewValue(atributs,post_id,a)
    except KeyError:
        return  "\U0001F632"
    for i in range(0,len(k)):
        k[i]=k[i].replace('_',' ')
    answer=text[3].lower()+" : "+', '.join(k)+" приписаны "+text[1]
    return answer

# новый баланс  пользователя
def NewMoney(text,vk,event):
    try:
        post_id=AllName[text[1]]
    except KeyError:
        return  "\U0001F632"
    money=database.HowManyMoney(post_id)
    if text[3][0]=="+" or text[3][0]=="-":
        money+=int(text[3])
    else:
        return "\U0001F632"
    if money<0:
        return "Невозможно! Ты врунишка! У тебя всего "+str(money-int(text[3]))+" денежных единиц."
    truechat=database.TrueDialog(post_id)

    if int(truechat)==int(event.object.peer_id):
        user_id=event.object.from_id
        master=database.HowIsBoss(post_id)
        if master!=user_id:
            SMSmaster=" Пользователь https://vk.com/id"+str(user_id)+" изменяет баланс "+text[1]+" на "+text[3]+" единиц"
            send.sendText(vk,master,SMSmaster)
        answer=database.NewMoney(money,post_id)
        return answer
    else:
        return " ты ошибся, милок"

# обмен деньгами между пользователями
def Broadcast(text,vk,event):
    try:
        post_id=AllName[text[3]]
        money=database.HowManyMoney(post_id)
        post_id2=AllName[text[4]]
        money2=database.HowManyMoney(post_id2)
    except KeyError:
        return  "\U0001F632"
    money-=int(text[2])
    money2+=int(text[2])
    if money<0:
        return "Невозможно! Ты врунишка! У тебя всего "+str(money+int(text[2]))+" денежных единиц."
    truechat=database.TrueDialog(post_id)
    if int(truechat)==int(event.object.peer_id):
        user_id=event.object.from_id
        master=database.HowIsBoss(post_id)
        if master!=user_id:
            SMSmaster=" Пользователь https://vk.com/id"+str(user_id)+" изменяет баланс "+text[1]+" на "+text[3]+" единиц"
            send.sendText(vk,master,SMSmaster)
        answer=database.NewMoney(money,post_id)+" "+text[3]+"\n"+database.NewMoney(money2,post_id2)+" "+text[4]
        return answer
    else:
        return " И не стыдно друзей обманывать?"
# модуль для очерёдности
def peremena(text):
    luck=text[2:]# берём полученный массив с людьми 
    random.shuffle(luck)#мешаем это в с помощью модуля рандом
    return " ".join(luck)#возвращаем это текстом через пробел 
# бросок одного кубика
def fate(text):
    answer=""
    bonus=0
    for i in range(0,4):
        answer+=random.choice("+- ")

    if len(text)>2:
        bonus=database.bonusFate(text[2],text[3:])
    for i in answer:
        if i=="+":
            bonus+=1
        if i=="-":
            bonus-=1
    answer+=" "+str(bonus)
    return answer

def cube(cube):
    if cube.isdigit():# роверяем является числом символ после буквы д
        if 0<int(cube)<=200:#больше ли оно 0 и меньше ли 100
            return str(random.randint(1,int(cube)))#выдаём рандомное число 
        else:
            return "\U0001F632"
    else:
        return "\U0001F632"
# бросок нескольких кубов 
def manycube(cub,flag=False):
    answer=[]
    summa=0
    a=0
    print(flag)
    for i in range(int(cub[0])):
        a=cube(cub[1])
        if a=="\U0001F632":#если запрашивают слишком большой куб посылать
            return"\U0001F632"
        if flag:
            summa=summa+int(a)
        answer.append(str(a))
    if flag:
        return "+".join(answer)+"="+str(summa)
    return " ".join(answer)
