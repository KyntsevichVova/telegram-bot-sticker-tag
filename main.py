import telegram, pymongo, json, handlers
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

with open('BOTINFO.json') as f:
    TOKEN = json.load(f)['TOKEN']

bot = telegram.Bot(token=TOKEN)
updater = Updater(token=TOKEN)

def main():
    print('Starting')
    dispatcher = updater.dispatcher
    
<<<<<<< HEAD
    dispatcher.add_handler(CommandHandler('addtag', handlers.add_tag))
    dispatcher.add_handler(CommandHandler('addtags', handlers.add_tags))

    dispatcher.add_handler(CommandHandler('removetag', handlers.remove_tag))
    dispatcher.add_handler(CommandHandler('removetags', handlers.remove_tags))

    dispatcher.add_handler(MessageHandler(Filters.sticker, handlers.handle_sticker))
    dispatcher.add_handler(CommandHandler('cancel', handlers.cancel))
=======
    dispatcher.add_handler(CommandHandler('addtag', handlers.addtag))
    dispatcher.add_handler(CommandHandler('addtags', handlers.addtags))

    dispatcher.add_handler(CommandHandler('removetag', handlers.removetag))
    dispatcher.add_handler(CommandHandler('removetags', handlers.removetags))

    dispatcher.add_handler(CommandHandler('cancel', handlers.cancel))
    dispatcher.add_handler(MessageHandler(Filters.sticker, handlers.handle_sticker))
>>>>>>> a73be6a079cbb0fd6acd0a211e3be2f44fd3b5c3

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()


