import logging

from db_utils import user_has_question, save_user_question, get_user_question, del_user_question
from utils import get_random_question

logger = logging.getLogger(__name__)


def get_new_question(db, user_id) -> str:
    if user_has_question(db, user_id):
        return 'Вы уже получили вопрос. Хотите сдаться?'

    logger.info('Generate random question')
    question = get_random_question()

    save_user_question(db, user_id, question)
    return question['question']


def give_up_and_get_solution(db, user_id) -> str:
    # TODO: Попрботать с этим методом.
    #  Чтобы у ботов не генерировался новый вопрос. Можно отправлять кортеж (boolean, str)
    question = get_user_question(db, user_id)

    if not question:
        return 'Не сдавайтесь. Для начала получите вопрос'

    del_user_question(db, user_id)

    return question["answer"]


def solution_attempt(db, user_id, answer) -> str:
    user_question = get_user_question(db, user_id)

    if not user_question:
        return 'Чтобы ответить на вопрос, надо его получить. Нажмите кнопку Новый вопрос'

    # TODO: Сделать проверку ответа умнее
    if user_question['answer'] == answer:
        del_user_question(db, user_id)
        return 'Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»'
    else:
        return 'Неправильно… Попробуешь ещё раз?'


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
