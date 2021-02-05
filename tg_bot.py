import logging
import os
import sys

import redis
import telegram
from dotenv import load_dotenv
from telegram.ext import CommandHandler, Updater, ConversationHandler, RegexHandler, MessageHandler, Filters

from db_utils import save_user_question, user_has_question, del_user_question, get_user_question
from utils import get_random_question

logger = logging.getLogger(__name__)

CHOOSE = range(1)


def get_user_id(update):
    return f'tg_{update.message.chat_id}'


def start_handler(bot, update):
    keyboard = [
        ['Новый вопрос', 'Сдаться'],
        ['Мой счет']
    ]

    reply_markup = telegram.ReplyKeyboardMarkup(keyboard)
    update.message.reply_text('Приветствую!', reply_markup=reply_markup)

    return CHOOSE


def handle_new_question_request(bot, update):
    user_id = get_user_id(update)

    if user_has_question(r, user_id):
        update.message.reply_text('Вы уже получили вопрос. Хотите сдаться?')
        return

    logger.info('Generate random question')
    question = get_random_question()

    save_user_question(r, user_id, question)
    update.message.reply_text(question['question'])

    logger.info('Message was send to chat_id={} with question: {}'.format(update.message.chat_id, question))


def handle_solution_attempt(bot, update):
    logger.info('Find answer in db')
    user_id = get_user_id(update)
    user_question = get_user_question(r, user_id)
    message_text = update.message.text

    if not user_question:
        update.message.reply_text('Чтобы ответить на вопрос, надо его получить. Нажмите кнопку Новый вопрос')
        return

    # TODO: Сделать проверку ответа умнее
    if user_question['answer'] == message_text:
        update.message.reply_text('Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»')
        del_user_question(r, user_id)
    else:
        update.message.reply_text('Неправильно… Попробуешь ещё раз?')


if __name__ == '__main__':
    load_dotenv()
    logging.basicConfig(level=logging.INFO)

    try:
        r = redis.Redis(host=os.getenv('REDIS_HOST'))
        r.ping()
    except redis.exceptions.RedisError as error:
        logger.error('Redis exception', exc_info=True)
        sys.exit(1)

    updater = Updater(os.getenv('TELEGRAM_BOT_TOKEN'))
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_handler)],
        states={
            CHOOSE: [RegexHandler('^Новый вопрос$', handle_new_question_request),
                     MessageHandler(Filters.text, handle_solution_attempt)],
        },
        fallbacks=[ConversationHandler.END]
    )

    dispatcher.add_handler(conv_handler)
    # dispatcher.add_handler(MessageHandler(Filters.text, message_handler))

    logger.info('Long polling started')
    updater.start_polling()

    updater.idle()
    logger.info('Bot stopped')
