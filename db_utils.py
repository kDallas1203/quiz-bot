import json
import logging

logger = logging.getLogger(__name__)


def get_user_question(db, user_id):
    logging.info(f'Find question for {user_id}')
    user_question_json = db.get(user_id)

    if not user_question_json:
        logging.info('Not found question for user {}'.format(user_id))
        return None

    user_question = json.loads(user_question_json)
    logging.info(f'Question {user_question} was find for user {user_id}')
    return user_question


def save_user_question(db, user_id, question):
    db.set(user_id, json.dumps(question))
    logger.info(f'Question {question} for user {user_id} saved')


def del_user_question(db, user_id):
    logger.info('Question for user {} deleted'.format(user_id))
    db.delete(user_id)


def user_has_question(db, user_id):
    return db.exists(user_id)
