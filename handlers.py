from pymongo import MongoClient, cursor
from telegram import InlineQueryResultCachedSticker
import re

print('Opening database')
client = MongoClient()
db = client['sticker-bot-db']['tags']

queries = {}

#modes:
# -1 : no queries from user
#  0 : last query == addtag
#  1 : last query == addtags
#  2 : last query == removetag
#  3 : last query == removetags

def remove_user(user):
    if user in queries:
        del queries[user]

def dump(message, tags):
    id = message.sticker.file_id
    user = message.from_user.username
    dumped = []
    global db
    for tag in tags:
        doc = {'user' : user, 'tag' : tag, 'sticker' : id}
        if db.find_one(doc) == None:
            db.insert_one(doc)
            dumped.append(tag)
    message.reply_text('OK, you added tags: ' + ', '.join(dumped))

def remove(message, tags):
    id = message.sticker.file_id
    user = message.from_user.username
    removed = []
    global db
    for tag in tags:
        doc = {'user' : user, 'tag' : tag, 'sticker' : id}
        if not db.find_one(doc) == None:
            db.delete_one(doc)
            removed.append(tag)
    message.reply_text('OK, you removed tags: ' + ', '.join(removed))

def add_tag(bot, update):
    global queries
    user = update.message.from_user.username
    if user not in queries:
        queries[user] = [[], -1]
    mode = queries[user][1]
    print('Add tag from ' + user)
    if mode == 0 or mode == 2 or mode == 3:
        update.message.reply_text('Error, you are supposed to send sticker now')
    else:
        ind = update.message.text.find(' ')
        text = update.message.text[ind:].strip()
        if ind == -1:
            text = ''
        if text == '':
            update.message.reply_text('Tag cannot be empty')
        else:
            queries[user][0].append(text)
            queries[user][1] = 0
            update.message.reply_text('OK, you are adding: ' + ', '.join(queries[user][0]))

def add_tags(bot, update):
    global queries
    user = update.message.from_user.username
    if user not in queries:
        queries[user] = [[], -1]
    mode = queries[user][1]
    print('Add tags from ' + user)
    if mode == 0 or mode == 2 or mode == 3:
        update.message.reply_text('Error, you are supposed to send sticker now')
    else:
        ind = update.message.text.find(' ')
        text = update.message.text[ind:].strip()
        if ind == -1:
            text = ''
        if text == '':
            update.message.reply_text('Tag cannot be empty')
        else:
            queries[user][0].append(text)
            queries[user][1] = 1
            update.message.reply_text('OK, you are adding: ' + ', '.join(queries[user][0]))

def remove_tag(bot, update):
    global queries
    user = update.message.from_user.username
    if user not in queries:
        queries[user] = [[], -1]
    mode = queries[user][1]
    print('Remove tag from ' + user)
    if mode == 0 or mode == 1 or mode == 2:
        update.message.reply_text('Error, you are supposed to send sticker now')
    else:
        ind = update.message.text.find(' ')
        text = update.message.text[ind:].strip()
        if ind == -1:
            text = ''
        if text == '':
            update.message.reply_text('Tag cannot be empty')
        else:
            queries[user][0].append(text)
            queries[user][1] = 2
            update.message.reply_text('OK, you are removing: ' + ', '.join(queries[user][0]))

def remove_tags(bot, update):
    global queries
    user = update.message.from_user.username
    if user not in queries:
        queries[user] = [[], -1]
    mode = queries[user][1]
    print('Remove tags from ' + user)
    if mode == 0 or mode == 1 or mode == 2:
        update.message.reply_text('Error, you are supposed to send sticker now')
    else:
        ind = update.message.text.find(' ')
        text = update.message.text[ind:].strip()
        if ind == -1:
            text = ''
        if text == '':
            update.message.reply_text('Tag cannot be empty')
        else:
            queries[user][0].append(text)
            queries[user][1] = 3
            update.message.reply_text('OK, you are removing: ' + ', '.join(queries[user][0]))

def handle_sticker(bot, update):
    global queries
    message = update.message
    user = message.from_user.username
    tags, mode = queries[user]
    print('Sticker ' + message.sticker.file_id + ' from ' + user)
    if mode == -1 or tags == []:
        message.reply_text('Please send tags first')
    elif mode == 0 or mode == 1:
        dump(message, tags)
    elif mode == 2 or mode == 3:
        remove(message, tags)
    remove_user(user)

def cancel(bot, update):
    remove_user(update.message.from_user.username)
    update.message.reply_text('Operations cancelled')

def inline_query(bot, update):
    query = update.inline_query
    print(query.from_user.username + ': ' + query.query)
    if not query.query:
        return
    stickers = db.find(
        filter={
            'user' : query.from_user.username, 
            'tag' : {'$regex': re.escape(query.query), '$options': 'i'}},
        limit=5)
    stickerset = {stickers[x]['sticker'] for x in range(stickers.count())}
    results = [InlineQueryResultCachedSticker(
        id=x,
        sticker_file_id=x
    ) for x in stickerset]
    print('Queried: ' + update.inline_query.answer(results, is_personal=True, cache_time=10))
