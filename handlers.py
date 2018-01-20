queries = {}

#modes:
# -1 : no queries from user
#  0 : last query == addtag
#  1 : last query == addtags
#  2 : last query == removetag
#  3 : last query == removetags

def remove_user(user):
    print(queries[user])
    print(list(queries.keys()))
    del queries[user]
    print(list(queries.keys()))

def dump(message, tags):
    message.reply_text(message.sticker.file_id + ' ' + ''.join(tags))

def remove(message, tags):
    message.reply_text(message.sticker.file_id + ' ' + ''.join(tags))

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
        text = update.message.text[len('/addtag'):].strip()
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
        text = update.message.text[len('/addtags'):].strip()
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
        text = update.message.text[len('/removetag'):].strip()
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
        text = update.message.text[len('/removetags'):].strip()
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
    reinitialize()
    update.message.reply_text('Operations cancelled')
