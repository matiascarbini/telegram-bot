import logging
import os
import json
import requests
import re
import urllib.request
import string
import random
import validators
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext

# creo carpeta temporal
import os
if os.path.exists('./tmp') == False:
  os.mkdir("./tmp")

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Variables globales
PRODUTION = os.environ.get('PRODUTION')
TOKEN = os.environ.get('TOKEN')
PORT = int(os.environ.get('PORT'))
URL_BASE = os.environ.get('URL_BASE')
DATA_JSON = os.environ.get('DATA_JSON')
BOT_TRAINER = os.environ.get('BOT_TRAINER')

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):    
    data = getDataLoad()

    reply_markup = getKeyboard('page')
    
    context.bot.send_message(
      chat_id = update.effective_chat.id,
      text = data['start']['text'],
      reply_markup=reply_markup,
      parse_mode=ParseMode.HTML
    )    

def nosotros(update, context):
    data = getDataLoad() 

    reply_markup = getKeyboard('init')
      
    context.bot.send_message(
      chat_id = update.effective_chat.id,
      text = data['nosotros']['text'],
      reply_markup=reply_markup,
      parse_mode=ParseMode.HTML
    )

def soluciones(update, context):
    data = getDataLoad()

    reply_markup = getKeyboard('solutions')

    context.bot.send_message(
      chat_id = update.effective_chat.id,
      text = data['soluciones']['text'],
      reply_markup=reply_markup,
      parse_mode=ParseMode.HTML
    )

def productos(update, context):
    data = getDataLoad()    

    reply_markup = getKeyboard('init')
      
    context.bot.send_message(
      chat_id = update.effective_chat.id,
      text = data['productos']['text'],
      parse_mode=ParseMode.HTML
    )
 
    for producto in data['productos']['detail']:      
      text = "<i>"+ producto["code"] + "</i>\n"      
      text = text + "<b>" + producto["title"] + "</b> \n"      
      text = text + "<i>" + producto["text"] + "</i> \n\n"
      text = text + "<b>" + producto["currency"] + " " + str(producto["price"]) + "</b> \n\n"
      text = text + "<a href='"+producto["url"]+"'> Ver Más </a> \n\n"
      text = text + producto["image"]

      context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = text,
        parse_mode=ParseMode.HTML
      )

    context.bot.send_message(
      chat_id = update.effective_chat.id,
      text = data['productos']['response']['end_list_products'],
      reply_markup=reply_markup,
      parse_mode=ParseMode.HTML
    )

def contacto(update, context):
    data = getDataLoad()
 
    reply_markup = getKeyboard('init')

    context.bot.send_message(
      chat_id = update.effective_chat.id,
      text = data['contacto']['text'],
      reply_markup=reply_markup,
      parse_mode=ParseMode.HTML
    )

def herramientas(update, context):
    data = getDataLoad()
 
    reply_markup = getKeyboard('init')

    context.bot.send_message(
      chat_id = update.effective_chat.id,
      text = data['herramientas']['text'],
      parse_mode=ParseMode.HTML
    )

    text = ''
    for herramienta in data['herramientas']['detail']:      
      text = text + "<b>" + herramienta["title"] + "</b>: <i>" + herramienta["text"] + "</i> \n <code>" + herramienta["command"] + "</code> \n\n"      
      
    context.bot.send_message(
      chat_id = update.effective_chat.id,
      text = text,
      parse_mode=ParseMode.HTML,
      reply_markup=reply_markup,
    )

def help(update, context):
    data = getDataLoad()
            
    reply_markup = getKeyboard('page')

    context.bot.send_message(
      chat_id = update.effective_chat.id,
      text = data['help']['text'],
      reply_markup=reply_markup,
      parse_mode=ParseMode.HTML
    ) 


def clickButton(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    if query.data == 'nosotros':
      nosotros(update, context)
    elif query.data == 'soluciones':
      soluciones(update, context)
    elif query.data == 'productos':
      productos(update, context)      
    elif query.data == 'contacto':
      contacto(update, context)
    elif query.data == 'herramientas':
      herramientas(update, context)      
    elif query.data == 'start':
      start(update, context)
    elif query.data == 'help':
      help(update, context)            
    else:
      solucionesDetail(update, context)

def solucionesDetail(update: Update, context: CallbackContext):
    query = update.callback_query    
    query.answer()
    
    data = getDataLoad()
    for solucion in data['soluciones']['detail']:
      if query.data == solucion['reference']:
        
        reply_markup = getKeyboard('init')

        context.bot.send_message(
          chat_id = update.effective_chat.id,
          text = solucion['text'],
          reply_markup=reply_markup,
          parse_mode=ParseMode.HTML
        )


def exec_br(update: Update, context: CallbackContext, urlImage="", chatID=0):
  try:
    data = getDataLoad()
        
    context.bot.send_message(
      chat_id = update.effective_chat.id,
      text = data['herramientas']['detail'][0]["response"]["after_request"],
      parse_mode=ParseMode.HTML
    )
    
    if urlImage:  
      image = urlImage
    else:
      image = ' '.join(context.args)      
    
    data_json = {"image":image}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post("http://179.43.121.48:301/background/remove", json = data_json, headers = headers)        
    res = r.text

    reply_markup = getKeyboard('init')
    if not chatID:
      sendChatID = update.effective_chat.id
    else:
      sendChatID = chatID
    
    if r.status_code == 200:          
      strRandom = ''
      number_of_strings = 5
      length_of_string = 8
      for x in range(number_of_strings):
        strRandom = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))
      
      filename = './tmp/image_without_background_' + strRandom + '.png'
      urllib.request.urlretrieve(res, filename)
      
      context.bot.send_document(
        chat_id=sendChatID, 
        document=open(filename, 'rb')
      )
 
      context.bot.send_message(
        chat_id = sendChatID,
        text = data['herramientas']['detail'][0]["response"]["request"] + ' ' + res,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
      )
    else:
      context.bot.send_message(
        chat_id = sendChatID,
        text = data['herramientas']['detail'][0]["response"]["error"],
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
      )  
  except:
    data = getDataLoad()
    
    reply_markup = getKeyboard('init')
    if not chatID:
      sendChatID = update.effective_chat.id   
    else:
      sendChatID = chatID
           
    context.bot.send_message(
      chat_id = sendChatID,
      text = data['herramientas']['detail'][0]["response"]["error"],
      reply_markup=reply_markup,
      parse_mode=ParseMode.HTML
    )             

def exec_sa(update: Update, context: CallbackContext):
  try:
    data = getDataLoad()
        
    context.bot.send_message(
      chat_id = update.effective_chat.id,
      text = data['herramientas']['detail'][1]["response"]["after_request"],
      parse_mode=ParseMode.HTML
    )
    
    text = ' '.join(context.args)
    
    reply_markup = getKeyboard('init')
    
    data_json = {"text":text}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post("http://179.43.121.48:300/sentiment-analysis/text", json = data_json, headers = headers)        
    res = json.loads(str(r.text))
    
    if r.status_code == 200:
      if res["sentimiento"] == 'POS':
        textResult = "<i>" + text + "</i> \n<b>POSITIVO</b>  --> " + res["probabilidades"]["positivo"] 
      
      if res["sentimiento"] == 'NEU':
        textResult = "<i>" + text + "</i> \n<b>NEUTRAL</b>  --> " + res["probabilidades"]["neutral"] 
        
      if res["sentimiento"] == 'NEG':
        textResult = "<i>" + text + "</i> \n<b>NEGATIVO</b>  --> " + res["probabilidades"]["negativo"] 
        
      context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = textResult,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
      )
    else:      
      context.bot.send_message(
        chat_id = update.effective_chat.id,        
        text = data['herramientas']['detail'][1]["response"]["error"],
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
      )       
  except:
    data = getDataLoad()
      
    reply_markup = getKeyboard('init')
      
    context.bot.send_message(
      chat_id = update.effective_chat.id,
      text = data['herramientas']['detail'][1]["response"]["error"],
      reply_markup=reply_markup,
      parse_mode=ParseMode.HTML
    )      

def exec_wc(update: Update, context: CallbackContext):
  try:
    data = getDataLoad()
        
    context.bot.send_message(
      chat_id = update.effective_chat.id,
      text = data['herramientas']['detail'][2]["response"]["after_request"],
      parse_mode=ParseMode.HTML
    )
    
    text = ' '.join(context.args)
    
    reply_markup = getKeyboard('init')
    
    data_json = {"user":text}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post("http://179.43.121.48:300/word-cloud/twitter/timeline", json = data_json, headers = headers)        
    res = r.text
    
    if r.status_code == 200:          
      strRandom = ''
      number_of_strings = 5
      length_of_string = 8
      for x in range(number_of_strings):
        strRandom = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))
      
      filename = './tmp/image_word_cloud_' + strRandom + '.png'
      urllib.request.urlretrieve(res, filename)
      
      context.bot.send_document(
        chat_id=update.effective_chat.id, 
        document=open(filename, 'rb')
      )
 
      context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = data['herramientas']['detail'][2]["response"]["request"] + ' ' + res,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
      )        
    else:      
      context.bot.send_message(
        chat_id = update.effective_chat.id,        
        text = data['herramientas']['detail'][2]["response"]["error"],
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
      )       
  except:
    data = getDataLoad()
      
    reply_markup = getKeyboard('init')
      
    context.bot.send_message(
      chat_id = update.effective_chat.id,
      text = data['herramientas']['detail'][2]["response"]["error"],
      reply_markup=reply_markup,
      parse_mode=ParseMode.HTML
    )           

def exec_bt(update: Update, context: CallbackContext):
  try:        
    trainer = getDataTrainer()
    data = getDataLoad()
    
    context.bot.send_message(
      chat_id = update.effective_chat.id,
      text = data['herramientas']['detail'][3]["response"]["after_request"],
      parse_mode=ParseMode.HTML
    )
        
    data_json = {"list":trainer.split("\n")}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post("http://179.43.121.48:300/chatbot/trainer", json = data_json, headers = headers)        
    
    if r.status_code == 200:          
      context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = data['herramientas']['detail'][3]["response"]["request"],      
        parse_mode=ParseMode.HTML
      )     
    else:      
      context.bot.send_message(
        chat_id = update.effective_chat.id,        
        text = data['herramientas']['detail'][3]["response"]["error"],
        parse_mode=ParseMode.HTML
      )       
  except:
    data = getDataLoad()   
      
    reply_markup = getKeyboard('init')
      
    context.bot.send_message(
      chat_id = update.effective_chat.id,
      text = data['herramientas']['detail'][3]["response"]["error"],
      reply_markup=reply_markup,
      parse_mode=ParseMode.HTML
    )        

def getKeyboard(renderKeyboard='init'):
    data = getDataLoad()

    keyboardPage = []
    keyboardSetting = []
    keyboardSolutions = []

    keyboardSetting.append([InlineKeyboardButton(data['start']['title'], callback_data=data['start']['reference'])])  
    keyboardSetting.append([InlineKeyboardButton(data['help']['title'], callback_data=data['help']['reference'])])  

    if data['nosotros']["show"] == True:
      keyboardPage.append([InlineKeyboardButton(data['nosotros']['title'], callback_data=data['nosotros']['reference'])])  

    if data['soluciones']["show"] == True:  
      keyboardPage.append([InlineKeyboardButton(data['soluciones']['title'], callback_data=data['soluciones']['reference'])])          

      for solucion in data['soluciones']['detail']:      
        keyboardSolutions.append([InlineKeyboardButton(solucion['title'], callback_data=solucion['reference'])])      

      keyboardSolutions.append([InlineKeyboardButton(data['start']['title'], callback_data=data['start']['reference'])])  
              
    if data['productos']["show"] == True:
      keyboardPage.append([InlineKeyboardButton(data['productos']['title'], callback_data=data['productos']['reference'])]) 
    
    if data['herramientas']["show"] == True: 
      keyboardPage.append([InlineKeyboardButton(data['herramientas']['title'], callback_data=data['herramientas']['reference'])]) 

    if data['contacto']["show"] == True: 
      keyboardPage.append([InlineKeyboardButton(data['contacto']['title'], callback_data=data['contacto']['reference'])]) 

    keyboardPage.append([InlineKeyboardButton(data['start']['title'], callback_data=data['start']['reference'])])  
    
    if renderKeyboard == 'init':
      reply_markup = InlineKeyboardMarkup(keyboardSetting)    
    elif renderKeyboard == 'page':
      reply_markup = InlineKeyboardMarkup(keyboardPage)    
    elif renderKeyboard == 'solutions':
      reply_markup = InlineKeyboardMarkup(keyboardSolutions)    
    else:
      reply_markup = InlineKeyboardMarkup(keyboardSetting)    

    return reply_markup


def getDataLoad():
  if validators.url(DATA_JSON):
    data = json.load(urllib.request.urlopen(DATA_JSON))
  else:
    f = open(DATA_JSON)    
    data = json.load(f)
    f.close
        
  return data

def getDataTrainer():
  if validators.url(BOT_TRAINER):
    data = urllib.request.urlopen(BOT_TRAINER).read().decode('utf-8')
  else:
    f = open(BOT_TRAINER, "r")    
    data = f.read()
    f.close()
      
  return data  
  

def echo(update, context):
    data = getDataLoad()
      
    bot = context.bot
    
    context.user_data["nombre"] = update.message.chat.first_name
    context.user_data["apellido"] = update.message.chat.last_name
    
    email = getEmail(update.message.text)
    if email:
      context.user_data["email"] = email
      
    phone = getPhone(update.message.text)
    if phone:
      context.user_data["telefono"] = phone
    
    if not email and not phone:
      response = getResposeMachineLearning(update.message.text)      
      if response:
        context.bot.send_message(
          chat_id = update.effective_chat.id,
          text = response,
          parse_mode=ParseMode.HTML
        )        
      else:    
        data = getDataLoad()
          
        reply_markup = getKeyboard('init')
          
        context.bot.send_message(
          chat_id = update.effective_chat.id,
          text = data['contacto']["response"]['default'],
          reply_markup=reply_markup,
          parse_mode=ParseMode.HTML
        )          
    else:
      if not 'email' in context.user_data.keys():
        context.user_data["email"] = '' 
        
      if not 'telefono' in context.user_data.keys():        
        context.user_data["telefono"] = '' 
      
      if context.user_data["email"] and not context.user_data["telefono"]:
        text=data['contacto']["response"]['only_email']
      elif not context.user_data["email"] and context.user_data["telefono"]:
        text=data['contacto']["response"]['only_phone']
      else:
        text=data['contacto']["response"]['all']
      
      bot.send_message(
        chat_id=update.message.chat_id, 
        text=text,
        parse_mode=ParseMode.HTML
      )      
      
def getResposeMachineLearning(text):
  try:    
    data_json = {"question":text}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post("http://179.43.121.48:300/chatbot/answer", json = data_json, headers = headers)        
    res = r.text
    
    if r.status_code == 200:          
      return res     
    else:      
      return ''
      
  except:
    return ''

  
def getEmail(text):
  email = ''
  arrData = text.split()
  for item in arrData:
    if re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$',item.lower()):
      email = item
  
  return email
  
def getPhone(text):
  phone = ''
  arrData = text.split()
  for item in arrData:    
    if all([x.isdigit() for x in item.split("-")]) and len(item)>5:
      phone = item
        
  return phone

def getImage(update, context):
  data = getDataLoad()
  
  if update.message.caption == "/" + data['herramientas']['detail'][0]["reference"]:        
    exec_br(update, context, context.bot.get_file(update.message.photo[-1]).file_path, update.message.chat.id)
  else:    
    reply_markup = getKeyboard('init')    
    bot = context.bot
    bot.send_message(
      chat_id=update.message.chat_id, 
      text=data['contacto']["response"]['default'],
      parse_mode=ParseMode.HTML,
      reply_markup=reply_markup
    )    

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    
    #obtengo el contenido
    data = getDataLoad()
    
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler(data['start']['reference'], start))    
    dp.add_handler(CommandHandler(data['nosotros']['reference'], nosotros))
    dp.add_handler(CommandHandler(data['soluciones']['reference'], soluciones))    
    dp.add_handler(CommandHandler(data['productos']['reference'], productos))    
    dp.add_handler(CommandHandler(data['contacto']['reference'], contacto))    
    dp.add_handler(CommandHandler(data['herramientas']['reference'], herramientas))    
    dp.add_handler(CommandHandler(data['help']['reference'], help))
    dp.add_handler(CommandHandler(data['herramientas']["detail"][0]['reference'], exec_br))
    dp.add_handler(CommandHandler(data['herramientas']["detail"][1]['reference'], exec_sa))
    dp.add_handler(CommandHandler(data['herramientas']["detail"][2]['reference'], exec_wc))
    dp.add_handler(CommandHandler(data['herramientas']["detail"][3]['reference'], exec_bt))
  
    # capturo el click
    updater.dispatcher.add_handler(CallbackQueryHandler(clickButton))
    
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))
    dp.add_handler(MessageHandler(Filters.photo, getImage))
    
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    if PRODUTION==False:        
      updater.start_polling()
    else:
      updater.start_webhook(listen="0.0.0.0", 
                            port=PORT, 
                            url_path=TOKEN,
                            webhook_url=URL_BASE + TOKEN)
      
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()