import logging
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = os.environ.get('TOKEN')
PORT = int(os.environ.get('PORT', '5000'))

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):    
    update.message.reply_text('Hola!')

def help(update, context):
    update.message.reply_text('Dejame ver como te ayudo!')

def hola(update, context):
    update.message.reply_text('Mostrito, como andas?? que contas???')

def chau(update, context):
    update.message.reply_text('Nos vemos mostro!!')    

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
    dp.add_handler(CommandHandler("hola", hola))
    dp.add_handler(CommandHandler("chau", chau))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    #updater.start_polling()
    updater.start_webhook(listen="0.0.0.0", 
                          port=PORT, 
                          url_path=TOKEN,
                          webhook_url="https://carsoft-telegram-bot.herokuapp.com/" + TOKEN)
  
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()