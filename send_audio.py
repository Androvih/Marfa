import requests
from random import randint
import vk_api
import speech_recognition as sr
import os
import sys
import pydub
vk_session = vk_api.VkApi(token='ec7bc06e26596facfc964a0dfc2a38aa07a7d678c554e36fb6b83fa2bdc73461d6487541a7b983542d31f')
vk = vk_session.get_api()
a=vk.docs.getMessagesUploadServer(type = 'audio_message',peer_id=70176118)
print(a)
afile = requests.post(a['upload_url'], files = {'file': open('Natalia.mp3', 'rb')}).json()['file']
doc = vk.docs.save(file = afile, title = 'Voice message')['audio_message']
print(doc)
vk.messages.send(peer_id = 70176118, random_id = randint(-2147483648, 2147483647), message = '', attachment = 'doc%s_%s'%(doc['owner_id'], doc['id']))


