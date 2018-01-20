import telegram, pymongo, json, Handlers
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

with open('BOTINFO.json') as f:
    TOKEN = json.load(f)['TOKEN']

bot = telegram.Bot(token=TOKEN)
updater = Updater(token=TOKEN)

def main():
    print('Starting')
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler('addtag', Handlers.addtag))
    dispatcher.add_handler(CommandHandler('addtags', Handlers.addtags))

    dispatcher.add_handler(CommandHandler('removetag', Handlers.removetag))
    dispatcher.add_handler(CommandHandler('removetags', Handlers.removetags))

    dispatcher.add_handler(CommandHandler('cancel', Handlers.cancel))
    dispatcher.add_handler(MessageHandler(Filters.sticker, Handlers.handle_sticker))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()


