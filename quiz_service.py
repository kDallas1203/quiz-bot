import logging
import random

from db_utils import (
    user_has_question,
    save_user_question,
    get_user_question,
    del_user_question
)
from exceptions import UserHasNoQuestion

logger = logging.getLogger(__name__)


def get_new_question(db, user_id, questions) -> str:
    if user_has_question(db, user_id):
        return 'Вы уже получили вопрос. Хотите сдаться?'

    logger.info(f'Generate random question for {user_id}')
    question = random.choice(list(questions.values()))

    save_user_question(db, user_id, question)
    return question['question']


def give_up_and_get_solution(db, user_id) -> str:
    question = get_user_question(db, user_id)

    if not question:
        raise UserHasNoQuestion()

    del_user_question(db, user_id)

    return question["answer"]


def solution_attempt(db, user_id, answer) -> str:
    user_question = get_user_question(db, user_id)

    if not user_question:
        raise UserHasNoQuestion()

    # TODO: Сделать проверку ответа умнее
    if user_question['answer'] == answer:
        del_user_question(db, user_id)
        return 'Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»'
    else:
        return 'Неправильно… Попробуешь ещё раз?'
