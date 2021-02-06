import json
import logging
import sys
import redis

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
    logger.info('Question for user {} saved'.format(user_id))


def del_user_question(db, user_id):
    logger.info('Question for user {} deleted'.format(user_id))
    db.delete(user_id)


def user_has_question(db, user_id):
    return db.exists(user_id)


def get_db_client(host, port) -> redis.Redis:
    try:
        db = redis.Redis(host=host, port=port)
        db.ping()
    except redis.exceptions.RedisError as error:
        logger.error('Redis exception', exc_info=True)
        sys.exit(1)

    return db


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
