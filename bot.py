import logging
import os
import json
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Variables globales
PRODUTION = os.environ.get('PRODUTION', False)
TOKEN = os.environ.get('TOKEN', '5087085476:AAEjL7-_iKsR8Z1KnIJp1yt4z2iDpHTktg8')
PORT = int(os.environ.get('PORT', '5000'))
URL_BASE = os.environ.get('URL_BASE','')
DATA_JSON = os.environ.get('DATA_JSON','data.json')

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):    
    f = open(DATA_JSON)    
    data = json.load(f)

    reply_markup = getKeyboard('page')
    
    context.bot.send_message(
      chat_id = update.effective_chat.id,
      text = data['start']['text'],
      reply_markup=reply_markup,
      parse_mode=ParseMode.HTML
    )    
    f.close()

def nosotros(update, context):
    f = open(DATA_JSON)    
    data = json.load(f)    

    reply_markup = getKeyboard('init')
      
    context.bot.send_message(
      chat_id = update.effective_chat.id,
      text = data['nosotros']['text'],
      reply_markup=reply_markup,
      parse_mode=ParseMode.HTML
    )

    f.close()

def soluciones(update, context):
    f = open(DATA_JSON)    
    data = json.load(f)

    reply_markup = getKeyboard('solutions')

    context.bot.send_message(
      chat_id = update.effective_chat.id,
      text = data['soluciones']['text'],
      reply_markup=reply_markup,
      parse_mode=ParseMode.HTML
    )
    f.close()    

def productos(update, context):
    f = open(DATA_JSON)    
    data = json.load(f)    

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
      text = 'Listado completo de productos',
      reply_markup=reply_markup,
      parse_mode=ParseMode.HTML
    )

    f.close()

def contacto(update, context):
    f = open(DATA_JSON)    
    data = json.load(f)
 
    reply_markup = getKeyboard('init')

    context.bot.send_message(
      chat_id = update.effective_chat.id,
      text = data['contacto']['text'],
      reply_markup=reply_markup,
      parse_mode=ParseMode.HTML
    )
    f.close()

def herramientas(update, context):
    f = open(DATA_JSON)    
    data = json.load(f)
 
    reply_markup = getKeyboard('init')

    context.bot.send_message(
      chat_id = update.effective_chat.id,
      text = data['herramientas']['text'],
      parse_mode=ParseMode.HTML
    )

    text = ''
    for herramienta in data['herramientas']['detail']:      
      text = text + "<b>" + herramienta["title"] + "</b>: " + herramienta["command"] + "\n"      
      
    context.bot.send_message(
      chat_id = update.effective_chat.id,
      text = text,
      parse_mode=ParseMode.HTML,
      reply_markup=reply_markup,
    )

    f.close()

def help(update, context):
    f = open(DATA_JSON)    
    data = json.load(f)
            
    reply_markup = getKeyboard('page')

    context.bot.send_message(
      chat_id = update.effective_chat.id,
      text = data['help']['text'],
      reply_markup=reply_markup,
      parse_mode=ParseMode.HTML
    )
    f.close()   

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
    
    f = open(DATA_JSON)    
    data = json.load(f)
    for solucion in data['soluciones']['detail']:
      if query.data == solucion['reference']:
        
        reply_markup = getKeyboard('init')

        context.bot.send_message(
          chat_id = update.effective_chat.id,
          text = solucion['text'],
          reply_markup=reply_markup,
          parse_mode=ParseMode.HTML
        )
    f.close()

def exec_br(update: Update, context: CallbackContext):
    context.bot.send_message(
      chat_id = update.effective_chat.id,
      text = "✂️ Borrando fondo de la imagen, tardará unos segundos...",
      parse_mode=ParseMode.HTML
    )
      
    image = ' '.join(context.args)

    reply_markup = getKeyboard('init')
    
    data_json = {"image":image}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post("http://179.43.121.48:301/background-remove", json = data_json, headers = headers)        
    res = r.text
        
    if r.status_code == 200:          
      context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = "Te envío la imagen sin fondo " + res,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
      )
    else:
      context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = "Algo salio mal!! intentá nuevamente",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
      )      

def exec_sa(update: Update, context: CallbackContext):
    context.bot.send_message(
      chat_id = update.effective_chat.id,
      text = "🔍 Analizando texto, aguardá unos segundos...",
      parse_mode=ParseMode.HTML
    )
    
    text = ' '.join(context.args)
    
    reply_markup = getKeyboard('init')
    
    data_json = {"text":text}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post("http://179.43.121.48:300/sentiment-analysis", json = data_json, headers = headers)        
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
          text = "Algo salio mal!! intentá nuevamente",
          reply_markup=reply_markup,
          parse_mode=ParseMode.HTML
        )      

def getKeyboard(renderKeyboard='init'):
    f = open(DATA_JSON)    
    data = json.load(f)

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

    f.close()    

    return reply_markup


def echo(update, context):
    update.message.reply_text(update.message.text)

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))    
    dp.add_handler(CommandHandler("nosotros", nosotros))
    dp.add_handler(CommandHandler("soluciones", soluciones))    
    dp.add_handler(CommandHandler("productos", productos))    
    dp.add_handler(CommandHandler("contacto", contacto))    
    dp.add_handler(CommandHandler("herramientas", herramientas))    
    dp.add_handler(CommandHandler("help", help))
    updater.dispatcher.add_handler(CallbackQueryHandler(clickButton))

    dp.add_handler(CommandHandler("exec_br", exec_br))
    dp.add_handler(CommandHandler("exec_sa", exec_sa))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    if PRODUTION==False:        
      updater.start_polling()
    else:
      updater.start_webhook(listen="0.0.0.0", 
                            port=PORT, 
                            url_path=TOKEN,
                            webhook_url=URL_BASE + "/" + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()