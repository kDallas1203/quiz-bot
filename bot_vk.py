import logging
import os
import random

import vk_api as vk
from dotenv import load_dotenv
from vk_api.keyboard import VkKeyboard
from vk_api.longpoll import VkLongPoll, VkEventType

from db_utils import get_db_client
from exceptions import UserHasNoQuestion
from quiz_service import get_new_question, give_up_and_get_solution, solution_attempt
from utils import get_user_id

logger = logging.getLogger(__name__)


def init_keyboard() -> VkKeyboard:
    keyboard = VkKeyboard()

    keyboard.add_button('Новый вопрос')
    keyboard.add_button('Сдаться')
    keyboard.add_line()
    keyboard.add_button('Мой счет')

    return keyboard


def send_keyboard(event, vk_api, keyboard) -> None:
    vk_api.messages.send(
        peer_id=event.user_id,
        random_id=random.randint(1, 1000),
        keyboard=keyboard.get_keyboard(),
        message='Клавиатура'
    )


def handle_new_question_request(event, vk_api):
    user_id = get_user_id(prefix='vk', user_id=event.user_id)

    question = get_new_question(db=r, user_id=user_id)

    vk_api.messages.send(
        user_id=event.user_id,
        message=question,
        random_id=random.randint(1, 1000)
    )


def handle_give_up(event, vk_api):
    user_id = get_user_id(prefix='vk', user_id=event.user_id)

    try:
        solution = give_up_and_get_solution(db=r, user_id=user_id)
    except UserHasNoQuestion:
        vk_api.messages.send(
            user_id=event.user_id,
            message='Не сдавайтесь. Для начала получите вопрос',
            random_id=random.randint(1, 1000)
        )
        return

    vk_api.messages.send(
        user_id=event.user_id,
        message=f'Правильный ответ: {solution}',
        random_id=random.randint(1, 1000)
    )

    handle_new_question_request(event, vk_api)


def handle_solution_attempt(event, vk_api):
    user_id = get_user_id('vk', event.user_id)
    try:
        solution_result = solution_attempt(db=r, user_id=user_id, answer=event.text)
    except UserHasNoQuestion:
        vk_api.messages.send(
            user_id=event.user_id,
            message='Получите вопрос, нажав кнопку "Новый вопрос"',
            random_id=random.randint(1, 1000)
        )
        return

    vk_api.messages.send(
        user_id=event.user_id,
        message=solution_result,
        random_id=random.randint(1, 1000)
    )


if __name__ == '__main__':
    load_dotenv()
    logging.basicConfig(level=logging.INFO)

    r = get_db_client(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), password=os.getenv('REDIS_PASSWORD'))

    vk_session = vk.VkApi(token=os.getenv('VK_API_KEY'))
    vk_api = vk_session.get_api()
    longopoll = VkLongPoll(vk_session)

    logger.info('Long poll started')
    for event in longopoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            logger.info(f'Receive message {event} from {event.user_id}')
            send_keyboard(event, vk_api, keyboard=init_keyboard())

            if event.text == 'Новый вопрос':
                handle_new_question_request(event, vk_api)
                continue

            if event.text == 'Сдаться':
                handle_give_up(event, vk_api)
                continue

            handle_solution_attempt(event, vk_api)
