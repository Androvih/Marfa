import command
import blackjack
import database


def main(text,vk,event):
    #функции боженьки ГМ
    AllName=list(database.AllName().keys()) # запрос к базе имён

    if (text[1][0]=='д' or text[1][0]=='d') and text[1].isalnum(): #броски кубов
        cube=text[1][1:]
        answer=command.cube(cube)
        return answer
    if ("д" in text[1] or"d" in text[1]) and text[1][0].isdigit() and len(text[1])<8:
        if "д" in text[1]:
            flag=0
            if len(text)==3:
                if text[2]=="сумма":
                    flag=True
            answer=command.manycube(text[1].split('д'),flag)
       
        return answer
    if text[1]=="фейт":
        answer=command.fate(text)
        return answer

    # для Fate
    #Вывод всей информации о пользователе
    if text[1] in AllName and len(text)==2:
        answer=database.AllInfo(text[1])
        return answer
    
                 
    

        # Если больше 2х слов
    if len(text)>2:
        
        # смена баланса пользователя
        if text[2]=="баланс" and len(text)>3:
            answer=command.NewMoney(text,vk,event)
            return answer
        # вывод баланса пользователя
        if text[2]=="баланс" and len(text)==3:
            answer=command.HowManyMoney(text)
            return answer
        # обмен деньгами между пользователями
        if text[1]=="передать":
            answer=command.Broadcast(text,vk,event)
            return answer  
        if int(event.object.peer_id)>2000000000:
            if text[1]=="новый" and text[2]=="пользователь":
                answer=command.NewUser(event.object)
                return answer
            if text[1]=="смена" and text[2]=="мастера":
                answer=command.NewMaster(text,vk,event)
                return answer
            if text[1]=="беседа" and text[2]=="on":
                answer=database.NewDialogs(vk,event)
                return answer
            if text[2]=="боевой" and text[3]=="режим":
                answer=database.CombatMode(text)
                return answer
            if text[2]=="пьёт" and text[3]=="кровь":
                answer=database.DrinkBlood(text)
                return answer
            if text[2] in ["стереть","записать", "изменить","ранен","лечится"]:
                if text[2]=="записать":
                    answer=command.NewValue(text,event)
                    return answer
                if text[2]=="стереть":
                    answer=command.DeleteValue(text,event)
                    return answer
                if text[2]=="изменить":
                    answer=command.TransformValue(text,event)
                    return answer
                if text[2]=="ранен":
                    answer=database.WoundValue(text)
                    return answer
                if text[2]=="лечится":
                    answer=database.HealValue(text)
                    return answer
   # не знаю пока что может делать мастер

#    if int(event.object.peer_id)<2000000000:
 #       if len(text)>2:
  #          if text[2] in ["стереть","запись","зло","добро"]:
   #             chatmaster=database.MasterChat(event.object.peer_id)
    #            print(chatmaster)
     #           if chatmaster!="Владыка не одобрит твоих действий":
      #              try:
       #                 if text[2]=="стереть":
        #                    answer=command.DeleteValue(text,chatmaster)
         #                   return answer
          #              if text[2]=="запись":
           #                 answer=command.NewValue(text,chatmaster)
            #                return answer
             #           if text[2]=="зло" or text[2]=="добро":
              #              answer=command.ChangeMorality(text,chatmaster)
               #             return answer
                #    except IndexError:
                 #       print("not admin")
#                else:
 #                   return chatmaster


        """
    # модуль блэкджека
    для игры в карты
    разобраться с этой функцией
    if text[1]=="бд" and len(text)>2:
        # начало новой игры
        if text[2]=="игра":
            command.NewGame(text,key)
        # выдача карты 
        if text[2]=="карту":
            blackjack.NewCard(key,keys)
        # переход к новому пользователю 
        if text[2]=="хватит":
            blackjack.Enough(key,keys)
        # расскрытие крупье
        if text[2]=="открыть" and text[3]=="крупье":
            blackjack.CroupierOpen(key,keys)
        # удаление  колоды 
        if text[2]=="удалить" and text[3]=="стол":
            blackjack.DeletTable(key)
        #если ничего не подошло отправить удивлённый смайлик
        else:
            return "\U0001F632"

    """
# бесполезные функции    
    # изи ответы на дежурные фразы
    if text[1]=="привет":
        return "Здравствуйте"
    if text[1]=="пока":
        return " До свидания"
    if text[1]=="спасибо":
        return "Пожалуйста"
    if text[1]=="молодец":
        return "Спасибо"
    if text[1]=="люди":
        answer=command.players(vk,event)
        return answer
    # выбор очерёдности 
    if text[1]=="рандом" and len(text)>2:
        answer=command.peremena(text)
        return answer
#


    return "\U0001F632"


