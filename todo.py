import json 
import requests
import time
import urllib
from dbhelper import DBHelper

db = DBHelper()
TOKEN = "831582668:AAHJQ6W3KcQvBPgE9-XUDwZjGH9qwueLJ6Y"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    # ensures that the messages that have been processed will not be processed again
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    # getting 'result' from the json object
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

def get_last_update_id(updates):
    # returns the highest id we get from all the updates
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def handle_updates(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        items = db.get_items(chat)
        if text == "/done":
            # asking to delete item
            keyboard = build_keyboard(items)
            send_message("Select an item to delete", chat, keyboard)
        elif text in items:
            # if text u send is alr in list, assume u want deletion
            db.delete_item(text,chat)
            items = db.get_items(chat)
            keyboard = build_keyboard(items)
            send_message("Select an item to delete", chat, keyboard)
        elif text == "/start":
            # start message
            send_message("Welcome to your personal To Do list. Send any text to me and I'll store it as an item. Send /done to remove items", chat)
        elif text.startswith("/"):
            # ignore all other '/' messages
            continue
        else:
            db.add_item(text,chat)
            items = db.get_items(chat)
            message = "\n".join(items)
            send_message(message, chat)

def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    # the keyboard is stored in the markup
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)

def build_keyboard(items):
    #turn each item into an entire row of the keyboard
    keyboard = [[item] for item in items]
    #keyboard disspears after a user makes a choice
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)
    

def main():
    db.setup()
    last_update_id = None
    while True:
        print("getting updates")
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
