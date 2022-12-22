from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler
import csv
import requests
from pprint import pprint

from config import *


def clock(context):
    otvet = {}
    with open('users.csv', 'r') as f:
        reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)
        for i in reader:
            if int(i[0]) == int(context.job.name):
                otvet = requests.get(f"http://api:{5001}/request", params={"data": i[-1].split()}).json()
                break

    for i in otvet:
        message = []
        message.append(" ".join(["*название:*", otvet[i].get("name", "Ошибка")]))
        message.append(" ".join(["*Цена в долларах*"]))
        message.append(" ".join([" ―  ", otvet[i].get("price_usd", {}).get("today"), "(за сегодня)"]))
        message.append(" ".join([" ―  ", otvet[i].get("price_usd", {}).get("per_day"), "(за 24 часа)"]))
        message.append(" ".join([" ―  ", otvet[i].get("price_usd", {}).get("per_week"), "(за 7 дней)"]))
        message.append(" ".join(["*Цена в BTC*"]))
        message.append(" ".join([" ―  ", otvet[i].get("price_btc", {}).get("today"), "(за сегодня)"]))
        message.append(" ".join([" ―  ", otvet[i].get("price_btc", {}).get("per_day"), "(за 24 часа)"]))
        message.append(" ".join([" ―  ", otvet[i].get("price_btc", {}).get("per_week"), "(за 7 дней)"]))
        message.append(" ".join(["*Капитализация*"]))
        message.append(" ".join([" ―  ", otvet[i].get("capitalization", {}).get("usd")]))
        message.append(" ".join([" ―  ", otvet[i].get("capitalization", {}).get("btc")]))
        message.append(" ".join(["*Объем обмена за 24 часа*"]))
        message.append(" ".join([" ―  ", otvet[i].get("exchange_volume_is_24h", {}).get("value")]))
        message.append(" ".join([" ―  ", otvet[i].get("exchange_volume_is_24h", {}).get("btc")]))
        message.append(" ".join([" ―  ", otvet[i].get("exchange_volume_is_24h", {}).get("usd")]))

        context.bot.send_message(
            chat_id=context.job.context, text="\n".join(message), parse_mode=ParseMode.MARKDOWN)


def remove_job_if_exists(name: str, context) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

def unsub(update, context):
    job_removed = remove_job_if_exists(str(update.message.chat_id), context)
    if job_removed:
        update.message.reply_text("Вы отписались")
    else:
        update.message.reply_text("У вас нет отписки, чтобы отписаться")

def sub(update, context):

    values = context.args

    data = []

    with open('users.csv', 'r') as f:
        reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)
        for i in reader:
            data.append(i)


    user = update.message.chat_id
    is_user = False
    for i in data:
        if int(i[0]) == int(user):
            i[1] = True
            i[2] = " ".join(values)
            is_user = True
            break

    if not is_user:
        data.append([user, 1, "None", " ".join(values)])
        data.append(["11"])

    with open('users.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';',
                                quotechar=';', quoting=csv.QUOTE_MINIMAL)

        for i in data:
            spamwriter.writerow(i)

    job_removed = remove_job_if_exists(str(update.message.chat_id), context)
    context.job_queue.run_repeating(clock, interval=5, context=update.message.chat_id, first=1, name=str(update.message.chat_id))
    update.message.reply_text("Вы подписались")


def start(update, context):
    update.message.reply_text("Это бот для мониторинга криптовалюты,\n  - используйте команду /sub (через пробел "
                              "аббривиатуры) Пример /sub BTC ETH\n  - Cайт мониторинга: https://bitinfocharts.com/ru/crypto-kurs/")


if __name__ == '__main__':
    upd = Updater(telegram_token, use_context=True)
    dp = upd.dispatcher
    jp = upd.job_queue

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('sub', sub))
    dp.add_handler(CommandHandler('unsub', unsub))

    #job_minute = jp.run_repeating(clock, interval=60, first=1)

    upd.start_polling()
    upd.idle()

