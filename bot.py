# -*- coding: utf-8 -*-
import telebot
from telebot import types
from telebot import util
import time
from time import sleep
import sys
import urllib2
import json
import urllib
import redis as r
reload(sys)
sys.setdefaultencoding("utf-8")
redis = r.StrictRedis(host='localhost', port=6379, db=0)
token = 'Token'
bot = telebot.TeleBot(token)

#Project Started!

@bot.message_handler(commands=['start','help'])
def start(m):
 id = m.from_user.id
 banlist = redis.sismember('blocked',id)
 if banlist == False:
  markup = types.InlineKeyboardMarkup()
  dev = types.InlineKeyboardButton(text='Developer',url='https://telegram.me/MosyDev')
  help = types.InlineKeyboardButton(text='Help',callback_data='help')
  markup.add(dev)
  markup.add(help)
  redis.sadd('users',m.from_user.id)
  bot.send_message(m.chat.id,'Hi {} Welcome To Php Code Checker Bot Just Send Your Source Code To Check It...!!\nOur Channels:\n@Cruel_News\n@MaxTeamCh'.format(m.from_user.first_name),reply_markup=markup)

#### Broadcast Message ####

@bot.message_handler(commands=['bc']) 
def broadcast(m): 
    if m.from_user.id ==  284244758 or m.from_user.id == 224976780: 
        text = m.text.replace("/bc ","") 
        rd = redis.smembers('users') 
        for id in rd: 
            try: 
                bot.send_message(id, "{}".format(text), parse_mode="html") 
            except: 
                print 'Netonestam bara bazia befrestam'

#### Banlist Handler ####

@bot.message_handler(commands=['banlist']) 
def banlist(m): 
    if m.from_user.id ==  284244758 or m.from_user.id == 224976780: 
        text = m.text.replace("/bc ","") 
        banlist = redis.smembers('blocked') 
        for id in banlist: 
                bot.send_message(m.chat.id,'Banlist:\n_({})_'.format(id),parse_mode='MarkDown')

#### FeedBack Method ####

@bot.message_handler(commands=['feedback'])
def feedback(m):
 try:
  text = m.text.replace('/feedback','')
  admin = 284244758
  admin2 = 224976780
  bot.send_message(m.chat.id,'Thanks dear For Your Feedback...!')
  bot.send_message(admin,'New FeedBack Form:\nUserName: {}\nFirst Name: {}\nFrom Id: {}\nFeedBack:\n{}\nAnswer It:\n/send {}'.format(m.from_user.username,m.from_user.first_name,m.from_user.id,text,m.from_user.id))
  bot.send_message(admin2,'New FeedBack Form:\nUserName: @{}\nFirst Name: {}\nFrom Id: {}\nFeedBack:\n{}\nAnswer It:\n/send {}'.format(m.from_user.username,m.from_user.first_name,m.from_user.id,text,m.from_user.id))
 except:
  bot.send_message(m.chat.id,'/feedback (Your FeedBack!)')

#### Answer FeedBack ####

@bot.message_handler(commands=['send'])
def send(m):
 if m.from_user.id == 284244758 or m.from_user.id == 224976780:
  id = m.text.split()[1]
  answer = m.text.split()[2]
  bot.send_message(id,answer)
  bot.send_message(m.chat.id,'Sent!')
#### Ban User ####

@bot.message_handler(commands=['ban'])
def ban(m):
 if m.from_user.id == 224976780 or m.from_user.id == 284244758:
  id = m.text.split()[1]
  redis.sadd('blocked',id)
  bot.send_message(m.chat.id,'User Blocked!')
  bot.send_message(id,'You Are Blocked!')

#### UnBan User ####

@bot.message_handler(commands=['unban'])
def ban(m):
 if m.from_user.id == 224976780 or m.from_user.id == 284244758:
  id = m.text.split()[1]
  redis.srem('blocked',id)
  bot.send_message(m.chat.id,'User Unblocked!')
  bot.send_message(id,'You Are Unblocked!')

#### Stats Of The Bot ####

@bot.message_handler(commands=['stats'])
def stats(m):
 id = m.from_user.id
 banlist = redis.sismember('blocked',id)
 if banlist == False:
  users = redis.scard('users')
  sources = redis.scard('code')
  bot.send_message(m.chat.id,'Users: {}\nSoures: {}'.format(users,sources))

#### Check Source Code ####

@bot.message_handler(content_types=['text'])
def check(msg):
 id = msg.from_user.id
 banlist = redis.sismember('blocked',id)
 if banlist == False:
  try:
      id = msg.from_user.id 
      code = msg.text
      msg = bot.send_message(msg.chat.id,'OK Please Wait Im Checking The Source Code!')
      redis.sadd('code',code)
      time.sleep(3)
      url ="http://phpcodechecker.com/api/?code={}".format(code)
      check = urllib.urlopen(url)
      data = check.read()
      jdat = json.loads(data)
      err = jdat['errors']
      result = jdat['syntax']['message']
      source = jdat['syntax']['code']
      bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text='Error Founded In Your Source!\nResult Is:\n*{}*'.format(result),parse_mode='Markdown')
  except ValueError:
   bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text='There Is No Error!')
  except KeyError:
   bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text='There Is No Error!')

#### Callback Data ####

@bot.callback_query_handler(func=lambda call: True) 
def callback_inline(call): 
  if call.message: 
     if call.data == "help":
      bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Hi dear, For Check Your Source Code Send Your Source Code To Me And I will be Check It..!!\n-----------------------\nDeveloper: @MosyDev\nChannels:\n@MaxTeamCh\n@Cruel_News")

#### Project Completed By @MosyDev ####

bot.polling(True)
