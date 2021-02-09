import logging
import os
import random
from os.path import join

logger = logging.getLogger(__name__)


def parse_blocks(file_content) -> dict:
    result = {}
    questions_blocks = []

    text_blocks = file_content.split('\n\n')

    for text_block in text_blocks:
        if 'Вопрос' in text_block or 'Ответ' in text_block:
            questions_blocks.append(text_block.strip('\n'))

    question_number = 1

    for num, question_block in enumerate(questions_blocks):
        if 'Ответ:' in question_block:
            question = ' '.join(questions_blocks[num - 1].split('\n')[1:])
            answer = ' '.join(question_block.split('\n')[1:])
            result[f'question_{question_number}'] = {'question': question, 'answer': answer}
            question_number += 1

    return result


def get_file_with_questions(path):
    logger.info('Open file from path {}'.format(path))
    with open(path, "r", encoding="KOI8-R") as _file:
        file_content = _file.read()
        _file.close()

    return file_content


def get_question_files_paths():
    current_dir = os.getcwd()
    paths = []
    for path, dirnames, filenames in os.walk(join(current_dir, 'questions')):
        for file in filenames:
            if file.endswith(".txt"):
                paths.append(os.path.join(path, file))

    return paths


def get_random_question() -> dict:
    files_path = get_question_files_paths()
    random_file_path = random.choice(files_path)
    blocks = get_file_with_questions(random_file_path)
    questions = parse_blocks(blocks)

    return random.choice(list(questions.values()))


def main():
    logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    main()
