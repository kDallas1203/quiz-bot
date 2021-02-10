import logging
import os

import redis
import telegram
from dotenv import load_dotenv
from telegram.ext import CommandHandler, Updater, ConversationHandler, RegexHandler, MessageHandler, Filters

from exceptions import UserHasNoQuestion
from quiz_service import get_new_question, give_up_and_get_solution, solution_attempt

logger = logging.getLogger(__name__)

CHOOSE = range(1)


def get_user_id_with_prefix(update):
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
    user_id = get_user_id_with_prefix(update)

    question = get_new_question(db=r, user_id=user_id)

    update.message.reply_text(question)

    logger.info('Message was send to chat_id={} with question: {}'.format(update.message.chat_id, question))


def handle_solution_attempt(bot, update):
    user_id = get_user_id_with_prefix(update)
    solution_result = solution_attempt(db=r, user_id=user_id, answer=update.message.text)
    update.message.reply_text(solution_result)


def handle_give_up(bot, update):
    user_id = get_user_id_with_prefix(update)
    solution = give_up_and_get_solution(db=r, user_id=user_id)
    update.message.reply_text(f'Правильный ответ: *"{solution}"*', parse_mode="Markdown")
    handle_new_question_request(bot, update)



def error(bot, update, error):
    logger.warning(f'Update {update} error "{error}"')

if __name__ == '__main__':
    load_dotenv()
    logging.basicConfig(level=logging.INFO)

    r = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), password=os.getenv('REDIS_PASSWORD'))
    r.ping()

    updater = Updater(os.getenv('TELEGRAM_BOT_TOKEN'))
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_handler),
                      RegexHandler('^Новый вопрос$', handle_new_question_request),
                      RegexHandler('^Сдаться$', handle_give_up),
                      MessageHandler(Filters.text, handle_solution_attempt)
                      ],
        states={
            CHOOSE: [RegexHandler('^Новый вопрос$', handle_new_question_request),
                     RegexHandler('^Сдаться$', handle_give_up),
                     MessageHandler(Filters.text, handle_solution_attempt)],
        },
        fallbacks=[ConversationHandler.END]
    )

    dispatcher.add_handler(conv_handler)
    dispatcher.add_error_handler(error)

    logger.info('Long polling started')
    updater.start_polling()

    updater.idle()
    logger.info('Bot stopped')
