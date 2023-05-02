# This Python file uses the following encoding: utf-8
import requests
from random import randint
import vk_api
import speech_recognition as sr
import pydub
import send
import command_main
import os
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
name=["марфа","марфонька","марфуня","марфута","марфуха","марфуша","марфеня","мара","маруша", "/"]
AudioMes=False
while (1):
	try:
		vk_session = vk_api.VkApi(token='')

		longpoll = VkBotLongPoll(vk_session,)
		vk = vk_session.get_api()
		for event in longpoll.listen():
			longpoll = VkBotLongPoll(vk_session,)
			print(event.object)
			if event.type == VkBotEventType.MESSAGE_NEW:
				try:
					if event.object.action['type']=="chat_invite_user":
						# Аудио записи до лучших времён
						#send.creatAudio("Здравствуй Путник. Моё имя Марфа. Я помощница и фамилиар Мастеров игры. Тебе я помогу определить свою судьбу броском кубика. Как общаться со мной ты можешь узнать на моей личной странице. https://vk.com/boginyakubov_off. Для корректной работы необходимо дать доступ ко всей переписке.")
						AudioMes=send.sendAudio(vk,event.object.peer_id,"Здравствуй Путник. Моё имя Марфа. Я помощница и фамилиар Мастеров игры. Тебе я помогу определить свою судьбу броском кубика. Как общаться со мной ты можешь узнать на моей личной странице. \u000D https://vk.com/boginyakubov_off. Для корректной работы необходимо дать доступ ко всей переписке.")
						continue
				except TypeError:
					pass

					# Аудио записи до лучших времён
				#try:
			#		if event.object.attachments[0]['type']=='audio_message':
			#			AudioMes=True
			#			link=event.object.attachments[0]['audio_message']['link_mp3']
			#			f=open(r'fucking_talk.mp3',"wb") #открываем файл для записи, в режиме wb
			#			ufr = requests.get(link) #делаем запрос
			#			f.write(ufr.content) #записываем содержимое в файл; как видите - content запроса
			#			f.close()
			#			sound = pydub.AudioSegment.from_mp3("fucking_talk.mp3")# переводим mp3 файл
			#			sound.export("fucking_talk.wav", format="wav")# в wav чтобы вытащить текст
			#			r = sr.Recognizer()
			#			with sr.WavFile("fucking_talk.wav") as source:
			#				r.pause_threshold = 1
			#				r.adjust_for_ambient_noise(source, duration=1)
			#				audio = r.listen(source)
			#			try:		
			#				inquiry = r.recognize_google(audio, language="ru-RU").lower()
			#			except sr.UnknownValueError:
			#				send.creatAudio("К сожалению, я вас не понимаю. Повторите ещё раз.")
			#				AudioMes=send.sendAudio(vk,event.object.peer_id,"К сожалению, я вас не понимаю. Повторите ещё раз.")
			#		else:
			#			if len(event.object.text)>0:
			#				inquiry=event.object.text
			#			else:
			#				continue

				if len(event.object.text)>0:
					inquiry=event.object.text
				else:
					continue
				# проверяем не пустое ли сообщение
				if inquiry[-1]=='.':# убираем точку если кто-то поставил её в конце
					inquiry=inquiry[:-1]
				inquiry=inquiry.split(' ')#разбиваем сообщения на элементы списка
				inquiry[0]=inquiry[0].lower()
				if inquiry[0] in name:#проверяем наличие слова-триггера
					if len(inquiry)==1:
						answer="Не марфкай"
					else:
						answer=command_main.main(inquiry,vk,event)#,AudioMes)#отправление сообщения на выполнение команд
					print(answer)
				#	if AudioMes:
			#			send.creatAudio(answer)
			#			AudioMes=send.sendAudio(vk,event.object.peer_id,answer)
			#		else:
					send.sendText(vk,event.object.peer_id,answer)
	except requests.exceptions.ReadTimeout:
		print("FUCK")
	except requests.exceptions.ConnectionError:
		print("FUCK")
