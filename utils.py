import logging
import os
from os.path import join
from uuid import uuid4

logger = logging.getLogger(__name__)


def parse_blocks(file_content) -> dict:
    result = {}
    questions_blocks = []

    text_blocks = file_content.split('\n\n')

    for text_block in text_blocks:
        if 'Вопрос' in text_block or 'Ответ' in text_block:
            questions_blocks.append(text_block.strip('\n'))

    for num, question_block in enumerate(questions_blocks):
        if 'Ответ:' in question_block:
            question = ' '.join(questions_blocks[num - 1].split('\n')[1:])
            answer = ' '.join(question_block.split('\n')[1:])
            result[f'question_{uuid4()}'] = {'question': question, 'answer': answer}

    return result


def get_file_with_questions(path):
    logger.info('Open file from path {}'.format(path))
    with open(path, "r", encoding="KOI8-R") as _file:
        file_content = _file.read()

    return file_content


def get_question_files_paths():
    current_dir = os.getcwd()
    paths = []
    for path, dirnames, filenames in os.walk(join(current_dir, 'questions')):
        for file in filenames:
            if file.endswith(".txt"):
                paths.append(os.path.join(path, file))

    return paths


def get_all_questions():
    questions = dict()

    files_path = get_question_files_paths()

    for file_path in files_path:
        blocks = get_file_with_questions(file_path)
        parsed_questions = parse_blocks(blocks)
        questions.update(parsed_questions)

    return questions
