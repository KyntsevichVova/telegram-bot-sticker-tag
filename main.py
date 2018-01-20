import telegram, pymongo, json, handlers
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

with open('BOTINFO.json') as f:
    TOKEN = json.load(f)['TOKEN']

bot = telegram.Bot(token=TOKEN)
updater = Updater(token=TOKEN)

def main():
    print('Starting')
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler('addtag', handlers.addtag))
    dispatcher.add_handler(CommandHandler('addtags', handlers.addtags))

    dispatcher.add_handler(CommandHandler('removetag', handlers.removetag))
    dispatcher.add_handler(CommandHandler('removetags', handlers.removetags))

    dispatcher.add_handler(CommandHandler('cancel', handlers.cancel))
    dispatcher.add_handler(MessageHandler(Filters.sticker, handlers.handle_sticker))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()


