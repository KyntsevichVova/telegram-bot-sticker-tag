import telegram, json, handlers
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

with open('BOTINFO.json') as f:
    TOKEN = json.load(f)['TOKEN']

bot = telegram.Bot(token=TOKEN)
updater = Updater(token=TOKEN)

def main():
    print('Starting')
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler('addtag', handlers.add_tag))
    dispatcher.add_handler(CommandHandler('addtags', handlers.add_tags))

    dispatcher.add_handler(CommandHandler('removetag', handlers.remove_tag))
    dispatcher.add_handler(CommandHandler('removetags', handlers.remove_tags))

    dispatcher.add_handler(MessageHandler(Filters.sticker, handlers.handle_sticker))
    dispatcher.add_handler(CommandHandler('cancel', handlers.cancel))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()


