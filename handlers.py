queries = {}

def remove_user(user):
    del queries[user]

def dump(message, tags):
    message.reply_text(message.sticker.file_id + ' ' + ''.join(tags))

def remove(message, tags):
    message.reply_text(message.sticker.file_id + ' ' + ''.join(tags))

def addtag(bot, update):
    print('Addtag from ' + update.message.from_user.username)
    global onetag_add, curtags_add
    if onetag_add:
        update.message.reply_text('Error, you are supposed to send sticker now')
    else:
        text = update.message.text[len('/addtag'):].strip()
        if text == '':
            update.message.reply_text('Tag cannot be empty')
        else:
            curtags_add.append(text)
            onetag_add = True
            update.message.reply_text('OK, you are adding: ' + ', '.join(curtags_add))

def addtags(bot, update):
    print('Addtags from ' + update.message.from_user.username)
    global onetag_add, curtags_add
    if onetag_add:
        update.message.reply_text('Error, you are supposed to send sticker now')
    else:
        text = update.message.text[len('/addtags'):].strip()
        if text == '':
            update.message.reply_text('Tag cannot be empty')
        else:
            curtags_add.append(text)
            update.message.reply_text('OK, you are adding: ' + ', '.join(curtags_add))

def removetag(bot, update):
    print('Addtag from ' + update.message.from_user.username)
    global onetag_rem, curtags_rem
    if onetag_rem:
        update.message.reply_text('Error, you are supposed to send sticker now')
    else:
        text = update.message.text[len('/addtag'):].strip()
        if text == '':
            update.message.reply_text('Tag cannot be empty')
        else:
            curtags_rem.append(text)
            onetag_rem = True
            update.message.reply_text('OK, you are adding: ' + ', '.join(curtags_rem))

def removetags(bot, update):
    print('Addtags from ' + update.message.from_user.username)
    global onetag_rem, curtags_rem
    if onetag_rem:
        update.message.reply_text('Error, you are supposed to send sticker now')
    else:
        text = update.message.text[len('/addtags'):].strip()
        if text == '':
            update.message.reply_text('Tag cannot be empty')
        else:
            curtags_rem.append(text)
            update.message.reply_text('OK, you are adding: ' + ', '.join(curtags_rem))

def handle_sticker(bot, update):
    global mode
    print('Sticker ' + update.message.sticker.file_id + ' from ' + update.message.from_user.username)
    if mode == -1:
        update.message.reply_text('Please send tags first')
    elif mode == 0:
        dump(update.message, tags)
    elif mode == 1:
        remove(update.message, tags)
    global curtags
    if curtags == []:
        update.message.reply_text('Please send tags first')
    dumptags(update.message, curtags)
    reinitialize()

def cancel(bot, update):
    reinitialize()
    update.message.reply_text('Operations cancelled')
