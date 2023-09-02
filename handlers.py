from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot import bot
import schedule
import threading
import config
from views import ReminderTexts

class Snooze:
    def __init__(self) -> None:
        self.cancel_tags = list()

class TempMessages:
    def __init__(self) -> None:
        self.to_delete = dict()

snooze = Snooze()
temp_messages = TempMessages()

def gen_markup(snooze):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton(ReminderTexts().took_medicine(), callback_data="done"),
                               InlineKeyboardButton(ReminderTexts().snooze(snooze), callback_data="snooze"))
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    tag = ReminderTexts().messages_tag()[call.message.text]
    cancel_reminder_schedule(tag)
    if call.data == "done":
        bot.edit_message_reply_markup(call.from_user.id, call.message.id)
        snooze.cancel_tags.append(tag)
        if tag in temp_messages.to_delete:
            for to_delete_message_id in temp_messages.to_delete.get(tag):
                bot.delete_message(call.from_user.id, to_delete_message_id)
            temp_messages.to_delete[tag] = list()
        bot.send_message(config.ADMIN_TELEGRAM_ID, "Clicked on done.")
    elif call.data == "snooze":
        threading.Timer(10 * 60, set_reminder_schedule, args=(2 * 60, beep, config.TARGET_TELEGRAM_ID, tag)).start()
        bot.answer_callback_query(call.id, "Snoozed")
        bot.send_message(config.ADMIN_TELEGRAM_ID, "Snoozed.")

def set_reminder_schedule(remind_each, job, telegram_id, tag):
    if tag in snooze.cancel_tags:
        snooze.cancel_tags.remove(tag)
        return
    
    schedule.every(remind_each).seconds.do(job, telegram_id, tag).tag(tag)

def cancel_reminder_schedule(tag):
    schedule.clear(tag)

def set_reminder(text, remind_each_minute, message_id):
    remind_each_second = remind_each_minute * 60
    bot.send_message(config.TARGET_TELEGRAM_ID, text, reply_markup=gen_markup(10))
    bot.send_message(config.ADMIN_TELEGRAM_ID, "Sent scheduled text.")
    set_reminder_schedule(remind_each_second, beep, config.TARGET_TELEGRAM_ID, message_id)



@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, ReminderTexts().start())

@bot.message_handler(commands=['woke_up'])
def woke_up(message):
    threading.Timer(0, set_reminder, args=(ReminderTexts().meds_before_breakfast_text(), 10, "meds_before_breakfast_text")).start()
    
    threading.Timer(15 * 60, set_reminder, args=(ReminderTexts().meds_12_hour_morning_text(), 5, "meds_12_hour_morning_text")).start()
    threading.Timer(12 * 60 * 60, set_reminder, args=(ReminderTexts().meds_12_hour_night_text(), 10, "meds_12_hour_night_text")).start()
    
    threading.Timer(15 * 60, set_reminder, args=(ReminderTexts().meds_8_hour_text(), 10, "meds_8_hour_text")).start()
    threading.Timer(7 * 60 * 60, set_reminder, args=(ReminderTexts().meds_8_hour_text(), 10, "meds_8_hour_text")).start()
    threading.Timer(14 * 60 * 60, set_reminder, args=(ReminderTexts().meds_8_hour_text(), 10, "meds_8_hour_text")).start()

    threading.Timer(15 * 60, set_reminder, args=(ReminderTexts().meds_6_hour_text(), 10, "meds_6_hour_text")).start()
    threading.Timer(5 * 60 * 60, set_reminder, args=(ReminderTexts().meds_6_hour_text(), 10, "meds_6_hour_text")).start()
    threading.Timer(10 * 60 * 60, set_reminder, args=(ReminderTexts().meds_6_hour_text(), 10, "meds_6_hour_text")).start()
    threading.Timer(14 * 60 * 60, set_reminder, args=(ReminderTexts().meds_6_hour_text(), 10, "meds_6_hour_text")).start()

    threading.Timer(12.01 * 60 * 60, set_reminder, args=(ReminderTexts().meds_night(), 10, "meds_night")).start()

    bot.send_message(config.ADMIN_TELEGRAM_ID, "Sent it.")

@bot.message_handler(commands=['launch'])
def launch(message):
    threading.Timer(0, set_reminder, args=(ReminderTexts().meds_meanwhile_launch(), 2, "meds_meanwhile_launch")).start()
    bot.send_message(config.ADMIN_TELEGRAM_ID, "Sent it.")

@bot.message_handler(commands=['dinner'])
def dinner(message):
    threading.Timer(0, set_reminder, args=(ReminderTexts().meds_meanwhile_dinner(), 2, "meds_meanwhile_dinner")).start()
    bot.send_message(config.ADMIN_TELEGRAM_ID, "Sent it.")



@bot.message_handler(commands=['only_meds_12_hour_morning'])
def only_meds_12_hour_morning(message):
    threading.Timer(0, set_reminder, args=(ReminderTexts().meds_12_hour_morning_text(), 2, "meds_12_hour_morning_text")).start()
    bot.send_message(config.ADMIN_TELEGRAM_ID, "Sent it.")

@bot.message_handler(commands=['only_meds_12_hour_night'])
def only_meds_12_hour_night(message):
    threading.Timer(0, set_reminder, args=(ReminderTexts().meds_12_hour_night_text(), 2, "meds_12_hour_night_text")).start()
    bot.send_message(config.ADMIN_TELEGRAM_ID, "Sent it.")

@bot.message_handler(commands=['only_meds_before_dinner'])
def only_meds_before_dinner(message):
    threading.Timer(0, set_reminder, args=(ReminderTexts().meds_before_dinner(), 2, "meds_before_dinner")).start()
    bot.send_message(config.ADMIN_TELEGRAM_ID, "Sent it.")

@bot.message_handler(commands=['only_meds_night'])
def only_meds_night(message):
    threading.Timer(0, set_reminder, args=(ReminderTexts().meds_night(), 2, "meds_night")).start()
    bot.send_message(config.ADMIN_TELEGRAM_ID, "Sent it.")

@bot.message_handler(commands=['only_meds_8_hour'])
def only_meds_8_hour(message):
    threading.Timer(0, set_reminder, args=(ReminderTexts().meds_8_hour_text(), 2, "meds_8_hour_text")).start()
    bot.send_message(config.ADMIN_TELEGRAM_ID, "Sent it.")

@bot.message_handler(commands=['only_meds_6_hour'])
def only_meds_6_hour(message):
    threading.Timer(0, set_reminder, args=(ReminderTexts().meds_6_hour_text(), 2, "meds_6_hour_text")).start()
    bot.send_message(config.ADMIN_TELEGRAM_ID, "Sent it.")


@bot.message_handler(content_types=['animation', 'audio', 'contact', 'dice', 'document', 'location', 'photo', 'poll', 'sticker', 'text', 'venue', 'video', 'video_note', 'voice'])
def log(message):
    bot.forward_message(config.LOG_GROUP_ID, message.chat.id, message.id)

def beep(chat_id, tag) -> None:
    """Send the beep message."""
    if tag not in temp_messages.to_delete:
        temp_messages.to_delete[tag] = list()
    temp_message = bot.send_message(chat_id, text=ReminderTexts().beep())
    temp_messages.to_delete[tag].append(temp_message.message_id)
    bot.send_message(config.ADMIN_TELEGRAM_ID, "Sent beep.")
