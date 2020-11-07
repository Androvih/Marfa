# This Python file uses the following encoding: utf-8
from rhvoice_wrapper import TTS
import vk_api
import requests
import os
import sys
from random import randint

def sendText(vk,sendId,text):
	vk.messages.send(peer_id=sendId,random_id = randint(-2147483648, 2147483647),message=text)

def sendAudio(vk,sendId,text=''):
	link=vk.docs.getMessagesUploadServer(type = 'audio_message',peer_id=sendId)
	vklink = requests.post(link['upload_url'], files = {'file': open('AudioAnswer.mp3', 'rb')}).json()['file']
	doc = vk.docs.save(file = vklink , title = 'Voice message')['audio_message']
	vk.messages.send(peer_id =sendId, random_id = randint(-2147483648, 2147483647), message =text, attachment = 'doc%s_%s'%(doc['owner_id'], doc['id']))
	return False

def creatAudio(say):
	tts = TTS(threads=1)
	tts.to_file(filename='AudioAnswer.mp3', text=say,voice='Anna', format_='mp3', sets=None)