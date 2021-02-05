import json
import logging

logger = logging.getLogger(__name__)


def get_user_question(r, user_id):
    user_question_json = r.get(user_id)

    if not user_question_json:
        logging.info('Not found question for user {}'.format(user_id))
        return None

    return json.loads(user_question_json)


def save_user_question(r, user_id, question):
    r.set(user_id, json.dumps(question))
    logger.info('Question for user {} saved'.format(user_id))


def del_user_question(r, user_id):
    logger.info('Question for user {} deleted'.format(user_id))
    r.delete(user_id)


def user_has_question(r, user_id):
    return r.exists(user_id)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
