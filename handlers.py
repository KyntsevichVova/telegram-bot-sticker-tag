from pymongo import MongoClient
from telegram import InlineQueryResultCachedSticker
from uuid import uuid4
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
#  4 : last query == showtags

def remove_user(user):
    if user in queries:
        del queries[user]

def dump(message, tags):
    id = message.sticker.file_id
    user = message.from_user.id
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
    user = message.from_user.id
    removed = []
    global db
    for tag in tags:
        doc = {'user' : user, 'tag' : tag, 'sticker' : id}
        if not db.find_one(doc) == None:
            db.delete_one(doc)
            removed.append(tag)
    message.reply_text('OK, you removed tags: ' + ', '.join(removed))

def show(message):
    global db
    records = db.find(filter={'user' : message.from_user.id, 'sticker' : message.sticker.file_id})
    tags = {records[x]['tag'] for x in range(records.count())}
    message.reply_text('Tags for sticker: ' + ', '.join(tags))

def add_tag(bot, update):
    global queries
    user = update.message.from_user
    if user.id not in queries:
        queries[user.id] = [[], -1]
    mode = queries[user.id][1]
    print('Add tag from {0} ({1})'.format(user.id, user.username))
    if mode == 0 or mode == 2 or mode == 3 or mode == 4:
        update.message.reply_text('Error, you are supposed to send sticker now')
    else:
        ind = update.message.text.find(' ')
        text = update.message.text[ind:].strip()
        if ind == -1:
            text = ''
        if text == '':
            update.message.reply_text('Tag cannot be empty')
        else:
            queries[user.id][0].append(text)
            queries[user.id][1] = 0
            update.message.reply_text('OK, you are adding: ' + ', '.join(queries[user.id][0]))

def add_tags(bot, update):
    global queries
    user = update.message.from_user
    if user.id not in queries:
        queries[user.id] = [[], -1]
    mode = queries[user.id][1]
    print('Add tags from {0} ({1})'.format(user.id, user.username))
    if mode == 0 or mode == 2 or mode == 3 or mode == 4:
        update.message.reply_text('Error, you are supposed to send sticker now')
    else:
        ind = update.message.text.find(' ')
        text = update.message.text[ind:].strip()
        if ind == -1:
            text = ''
        if text == '':
            update.message.reply_text('Tag cannot be empty')
        else:
            queries[user.id][0].append(text)
            queries[user.id][1] = 1
            update.message.reply_text('OK, you are adding: ' + ', '.join(queries[user.id][0]))

def remove_tag(bot, update):
    global queries
    user = update.message.from_user
    if user.id not in queries:
        queries[user.id] = [[], -1]
    mode = queries[user.id][1]
    print('Remove tag from {0} ({1})'.format(user.id, user.username))
    if mode == 0 or mode == 1 or mode == 2 or mode == 4:
        update.message.reply_text('Error, you are supposed to send sticker now')
    else:
        ind = update.message.text.find(' ')
        text = update.message.text[ind:].strip()
        if ind == -1:
            text = ''
        if text == '':
            update.message.reply_text('Tag cannot be empty')
        else:
            queries[user.id][0].append(text)
            queries[user.id][1] = 2
            update.message.reply_text('OK, you are removing: ' + ', '.join(queries[user.id][0]))

def remove_tags(bot, update):
    global queries
    user = update.message.from_user
    if user.id not in queries:
        queries[user.id] = [[], -1]
    mode = queries[user.id][1]
    print('Remove tags from {0} ({1})'.format(user.id, user.username))
    if mode == 0 or mode == 1 or mode == 2 or mode == 4:
        update.message.reply_text('Error, you are supposed to send sticker now')
    else:
        ind = update.message.text.find(' ')
        text = update.message.text[ind:].strip()
        if ind == -1:
            text = ''
        if text == '':
            update.message.reply_text('Tag cannot be empty')
        else:
            queries[user.id][0].append(text)
            queries[user.id][1] = 3
            update.message.reply_text('OK, you are removing: ' + ', '.join(queries[user.id][0]))

def show_tags(bot, update):
    global queries
    user = update.message.from_user
    if user.id not in queries:
        queries[user.id] = [[], -1]
    mode = queries[user.id][1]
    print('Show tags to {0} ({1})'.format(user.id, user.username))
    if mode != -1:
        update.message.reply_text('Error, you are supposed to send sticker now')
    else:
        queries[user.id][1] = 4
        update.message.reply_text('OK, now send me sticker')

def handle_sticker(bot, update):
    global queries
    message = update.message
    user = message.from_user
    tags, mode = queries[user.id]
    print('Sticker {0} from {1} ({2})'.format(message.sticker.file_id, user.id, user.username))
    if mode == -1 or (mode != 4 and tags == []):
        message.reply_text('Please send tags first')
    elif mode == 0 or mode == 1:
        dump(message, tags)
    elif mode == 2 or mode == 3:
        remove(message, tags)
    elif mode == 4:
        show(message)
    remove_user(user.id)

def cancel(bot, update):
    remove_user(update.message.from_user.id)
    update.message.reply_text('Operations cancelled')

def inline_query(bot, update):
    query = update.inline_query
    if not query.query:
        return
    print('Query \'{0}\' from {1} ({2})'.format(query.query, query.from_user.id, query.from_user.username))
    stickers = db.find(
        filter={
            'user' : query.from_user.id, 
            'tag' : {'$regex': re.escape(query.query), '$options': 'i'}},
        limit=5)
    stickerset = {stickers[x]['sticker'] for x in range(stickers.count())}
    results = [InlineQueryResultCachedSticker(
        id=uuid4(),
        sticker_file_id=x
    ) for x in stickerset]
    print('Queried: ' + update.inline_query.answer(results, is_personal=True, cache_time=10))
