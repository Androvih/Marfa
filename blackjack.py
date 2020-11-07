import requests
import random
token="4432efdef0141c7c518532fcd64a4a3e35a8e2244b5713efe434df0052be51b591627fc1079f5fc9db505"
url="https://api.vk.com/method/"
blackjack={}# создаём переменную для хранения игр
#блок подсчёта карт 
def Cards(cards):
    ace=0#количество тузов
    result=0#итоговый счёт  
    cards.sort()# сортируем карты от меньшей к большей
    for card in cards:
        if card in "ВДК":#если карта валет король или дама, результат +10
            result+=10
        elif card=="Т":#если туз
            ace+=1#увеличить колво тузов
            if (result+11)<=21:#если результат +11 меньше 21 
                result+=11#туз равен 11 очкам
            else:
                result+=1# иначе 1 очко 
        else:
            result+=int(card)# остальные карты по своим очкам
    if len(cards)==2 and ace==2:# если выпало два туза то это золотое очко
        result=21
    return result
def NewGame(play,chat_id,diller):
    if chat_id in blackjack:# если в беседке уже играли в карты
        if len(blackjack[chat_id][0])<20:# проверить количество карт, если мало добавить
            deck=["2","3","4","5","6","7","8","9","10","В","Д","К","Т"]*4#оздаём колоду
            random.shuffle(deck)# перемешиваем её
            deck.extend(blackjack[chat_id][0])# добавляем к новой колоде остаток от прошлой
            blackjack[chat_id][0]=deck# записываем её в колоду беседы
    else:
        blackjack[chat_id]=[]# создаём список по id беседы для игры
        deck=["2","3","4","5","6","7","8","9","10","В","Д","К","Т"]*4
        random.shuffle(deck)
        blackjack[chat_id].append(deck)
    NameId={}#создаём необходимые для игры словари
    Name={}
    Player={}
    t=requests.get('https://api.vk.com/method/messages.getChatUsers?chat_id='+str(chat_id)+'&fields=name&access_token='+token+'&v=5.68')# запрос о людях в беседе
    i=0
    for profil in ( t.json()['response']):
        if str(profil["id"])!="429544198":#заполнение словарей связаннй информацией, всех кроме Марфы
            NameId[str(i)]=str(profil["first_name"])
            Name[str(profil["id"])]=str(i)
            Player[str(profil["first_name"])]=str(profil["id"])
            i+=1
    blackjack[chat_id].append({})#создаём дополнительные поля для игры 
    blackjack[chat_id].append({})
    blackjack[chat_id].append({})
    blackjack[chat_id].append({})
    blackjack[chat_id].append(int(0))
    blackjack[chat_id][2]=NameId# передаём в них недавно созданные словари
    blackjack[chat_id][3]=Name
    blackjack[chat_id][4]=Player
    blackjack[chat_id].append(play)

    for nick in play:# вытаскиваем псевдо айди
        k=" "
        if nick in blackjack[chat_id][1]:# если введённое псевдоайди не найденно удаляем всё и сообщаем об ошибке
            j=0
            while j!=4:
                blackjack[chat_id].pop()
                j+=1
            requests.get("https://api.vk.com/method/messages.send?chat_id="+str(chat_id)+"&message=Ошибка! игрок не может повторятся&access_token="+token+"&v=5.64")
            return 
        blackjack[chat_id][1][nick]=[]# создаём в словаре пустой список
        blackjack[chat_id][1][nick].append([])#добавляем в список элемент список
        blackjack[chat_id][1][nick][0].append(blackjack[chat_id][0].pop())# засовываем в него две верхнии карты из колоды,
        blackjack[chat_id][1][nick][0].append(blackjack[chat_id][0].pop())#удаляя их оттуда
        blackjack[chat_id][1][nick].append(Cards(blackjack[chat_id][1][nick][0]))# добавляем в список количество полученных очков
        k=" ".join(blackjack[chat_id][1][nick][0])
        requests.get("https://api.vk.com/method/messages.send?user_id="+str(blackjack[chat_id][4][blackjack[chat_id][2][nick]])+"&message=Карты "+blackjack[chat_id][2][nick]+": "+k+" Счёт: "+str(blackjack[chat_id][1][nick][1])+"&access_token="+token+"&v=5.64")# отправляем пользователю его карты и счёт
    if diller in blackjack[chat_id][1]:#анологично с крупье, только всем игрокам показываем вторую карту крупье
        j=0
        while j!=4:
            blackjack[chat_id].pop()
            j+=1
        requests.get("https://api.vk.com/method/messages.send?chat_id="+str(chat_id)+"&message=Ошибка! игрок не может повторятся&access_token="+token+"&v=5.64")
        return 
    blackjack[chat_id][6].append(diller)
    blackjack[chat_id][1][diller]=[]
    blackjack[chat_id][1][diller].append([])
    blackjack[chat_id][1][diller][0].append(blackjack[chat_id][0].pop())
    blackjack[chat_id][1][diller][0].append(blackjack[chat_id][0].pop())
    requests.get("https://api.vk.com/method/messages.send?chat_id="+str(chat_id)+"&message=У крупье открыта карта "+str(blackjack[chat_id][1][diller][0][1])+"&access_token="+token+"&v=5.64")
    print("Game Start")            
#получение дополнительной карты
def NewCard(chat_id,NumberMessage):
    k=" "
    t=requests.get("https://api.vk.com/method/messages.getById?message_ids="+str(NumberMessage)+"&access_token="+token+"&v=5.71")#по номеру сообщения берём id пользователя
    user_id=t.json()["response"]["items"][0]["user_id"]
    try:
        if int(blackjack[chat_id][3][str(user_id)])==int(blackjack[chat_id][6][0]):# если оно совпадает со следующим по очереди
            blackjack[chat_id][1][blackjack[chat_id][3][str(user_id)]][0].append(blackjack[chat_id][0].pop())#то добавляем пользователю карту
            blackjack[chat_id][1][blackjack[chat_id][3][str(user_id)]][1]=Cards(blackjack[chat_id][1][blackjack[chat_id][3][str(user_id)]][0])# делаем пресчёт очков
            k=" ".join(blackjack[chat_id][1][blackjack[chat_id][3][str(user_id)]][0])
            if blackjack[chat_id][5]==1:# если сейчас играет крупье  отправлять карты в беседу
                requests.get("https://api.vk.com/method/messages.send?chat_id="+str(chat_id)+"&message=Карты "+str(blackjack[chat_id][2][blackjack[chat_id][3][str(user_id)]])+": "+k+" Счёт: "+str(blackjack[chat_id][1][blackjack[chat_id][3][str(user_id)]][1])+"&access_token="+token+"&v=5.64")
            else:# если пользователю, то ему в личку, а остальным имформацию лб этом
                requests.get("https://api.vk.com/method/messages.send?user_id="+str(user_id)+"&message=Карты "+str(blackjack[chat_id][2][blackjack[chat_id][3][str(user_id)]])+": "+k+" Счёт: "+str(blackjack[chat_id][1][blackjack[chat_id][3][str(user_id)]][1])+"&access_token="+token+"&v=5.64")
                requests.get("https://api.vk.com/method/messages.send?chat_id="+str(chat_id)+"&message=Игрок "+str(blackjack[chat_id][2][blackjack[chat_id][3][str(user_id)]])+" получил карту&access_token="+token+"&v=5.64")
            print("Card Get")
        else:
            requests.get("https://api.vk.com/method/messages.send?chat_id="+str(chat_id)+"&message=Куда лапы!&access_token="+token+"&v=5.64")
    except KeyError:
            requests.get("https://api.vk.com/method/messages.send?chat_id="+str(chat_id)+"&message=Ваша игра не найдена&access_token="+token+"&v=5.64")        
#открываем игрокам карты крупье
def CroupierOpen(chat_id,NumberMessage):
    k=" "
    t=requests.get("https://api.vk.com/method/messages.getById?message_ids="+str(NumberMessage)+"&access_token="+token+"&v=5.68")
    user_id=t.json()["response"]["items"][0]["user_id"]
    try:
        if int(blackjack[chat_id][6][-1])==int(blackjack[chat_id][3][str(user_id)]):#если обращающийся крупье
            blackjack[chat_id][1][blackjack[chat_id][3][str(user_id)]].append(Cards(blackjack[chat_id][1][blackjack[chat_id][3][str(user_id)]][0]))
            k=" ".join(blackjack[chat_id][1][blackjack[chat_id][3][str(user_id)]][0])#считаем карты и выводим их в беседу
            blackjack[chat_id][5]=1#отмечаем что следующее хватит заканчивает игру
            requests.get("https://api.vk.com/method/messages.send?chat_id="+str(chat_id)+"&message=Карты "+str(blackjack[chat_id][2][blackjack[chat_id][3][str(user_id)]])+": "+k+" Счёт: "+str(blackjack[chat_id][1][blackjack[chat_id][3][str(user_id)]][1])+"&access_token="+token+"&v=5.64")
        else:
            requests.get("https://api.vk.com/method/messages.send?chat_id="+str(chat_id)+"&message=Куда лапы!&access_token="+token+"&v=5.64")
    except KeyError:
        requests.get("https://api.vk.com/method/messages.send?chat_id="+str(chat_id)+"&message=Ваша игра не найдена&access_token="+token+"&v=5.64")        
#передача хода или завершение игры
def Enough(chat_id,NumberMessage):
    t=requests.get("https://api.vk.com/method/messages.getById?message_ids="+str(NumberMessage)+"&access_token="+token+"&v=5.68")
    user_id=t.json()["response"]["items"][0]["user_id"]
    try: 
        if int(blackjack[chat_id][6][0])==int(blackjack[chat_id][3][str(user_id)]):#если  очерёдность совпадает с опращающимся
            if len(blackjack[chat_id][6])>1:# сказать чей ход если сейчас не крупье
                requests.get("https://api.vk.com/method/messages.send?chat_id="+str(chat_id)+"&message=Игрок "+str(blackjack[chat_id][2][blackjack[chat_id][3][str(user_id)]])+" закончил набор. Следующий игрок "+str(blackjack[chat_id][2][blackjack[chat_id][6][1]])+"&access_token="+token+"&v=5.64")
            blackjack[chat_id][6].pop(0)#далить первого в очереди
        else:
            requests.get("https://api.vk.com/method/messages.send?chat_id="+str(chat_id)+"&message=Куда лапы!&access_token="+token+"&v=5.64")
        if blackjack[chat_id][5]==1:# если крупье сказал хватит
            point=0
            result=""
            name=blackjack[chat_id][1].keys()#берём ключи 
            for key in name:#подготовливаем результаты
                k=" ".join(blackjack[chat_id][1][key][0])
                point=Cards(blackjack[chat_id][1][key][0])
                result+=" Карты "+blackjack[chat_id][2][key]+": "+k+" Счёт: "+str(point)
            requests.get("https://api.vk.com/method/messages.send?chat_id="+str(chat_id)+"&message="+result+".&access_token="+token+"&v=5.64")
            i=int(1)#после отправления результатов чистим всё кроме колоды
            while i!=7:
                blackjack[chat_id].pop()
                i+=1
            print("End Game")
    except KeyError:
        requests.get("https://api.vk.com/method/messages.send?chat_id="+str(chat_id)+"&message=Ваша игра не найдена&access_token="+token+"&v=5.64")
#быстрое завершение игры + удаление колоды 
def DeletTable(chat_id):
    del blackjack[chat_id]