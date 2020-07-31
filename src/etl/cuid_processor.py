from pathlib import Path

import argparse
import json
import re
import os
import sys


flags = None


def warn(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('data', nargs='*', help='Original files to process')
    parser.add_argument('--output', '-o', help='Output to write the dataset')
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args()


def parse_preamble(lines):
    preamble = re.compile(
        r'^\s?(?:a\.\s?prueba de)?\s?comprensión lectora',
        re.IGNORECASE
    )
    text, index = '', 0
    for idx, line in enumerate(lines):
        match = re.match(preamble, line)
        if match is not None:
            text = match
            index = idx + 1
            break
    if index == 0:
        warn('Unable to find preamble to test')
    return text, index


def extract_tasks(lines):
    tasks = []
    task_indices = [0]
    nof_tasks = 0
    task_re = re.compile(
        r'^(?:\t\s)?tarea\s?\d+?',
        re.IGNORECASE | re.MULTILINE
    )
    for idx, line in enumerate(lines):
        match = re.match(task_re, line)
        if match is not None:
            if nof_tasks > 0:
                # consume task title and statement
                tasks.append(lines[task_indices[-1]+2:idx])
                task_indices.append(idx)
            nof_tasks += 1
    if nof_tasks != len(tasks):
        tasks.append(lines[task_indices[-1]+2:len(lines)])
    return tasks, len(lines)


def parse_article(lines):
    article = ''
    index = 0
    article_re = re.compile(r'\s?cuestiones\s?', re.IGNORECASE)
    for idx, line in enumerate(lines):
        match = re.match(article_re, line)
        if match is not None:
            article = '\n'.join(lines[:idx])
            index = idx
            break
    return article, index


def parse_questions_and_answers(lines):
    start_idx = 0
    questions, options, answers = [], [], []
    current_options = []
    question_re = re.compile(r'^\s?(?:\(\d+\)|\d+\.)\s?(.*)$')
    option_re = re.compile(r'^\s?(x)?(a|b|c|d)\.\s?(.*)$', re.IGNORECASE)
    question_start_re = re.compile(r'\s?cuestiones\s?', re.IGNORECASE)
    if re.match(question_start_re, lines[0]) is not None:
        start_idx += 1
    for line in lines:
        question = question_re.findall(line)
        if len(question) > 0:
            questions.append(question[0])
            if len(current_options) > 0:
                options.append(current_options)
            current_options = []
        else:
            # ('X?', 'a|b|c|d', 'answer text')
            option_tuple = option_re.findall(line)
            if len(option_tuple) > 0:
                option_tuple = option_tuple[0]
                if option_tuple[0].lower() == 'x':
                    answers.append(option_tuple[1].upper())
                current_options.append(option_tuple[-1])
    options.append(current_options)
    assert(len(questions) == len(options) == len(answers))
    return questions, options, answers


def parse_exam(full_text, exam_index=0):
    # exam = Exam()
    full_text_lines = [
        line.strip() for line in full_text.strip().split('\n') if line != ''
    ]
    _, index = parse_preamble(full_text_lines)
    tasks, index = extract_tasks(full_text_lines[index:])
    exam = []
    for task in tasks:
        try:
            article, index = parse_article(task)
            qas = task[index:]
            questions, options, answers = parse_questions_and_answers(qas)
            exam.append(dict(
                article=article,
                questions=questions,
                options=options,
                answers=answers,
                id=exam_index + len(exam)
            ))
        except Exception as e:
            warn('Dropping task, unable to parse', str(e))
    return exam


def main():
    exams = []
    for path in flags.data:
        warn('Processing {}'.format(path))
        full_text = open(path, 'r').read()
        exams.extend(parse_exam(full_text, len(exams)))
    warn('Total nof tasks {}'.format(len(exams)))
    file = ' | '.join([os.path.basename(p) for p in flags.data])
    full_exam = dict(version='1.0.0', file=file, data=exams)
    full_exam_str = json.dumps(obj=full_exam, ensure_ascii=False) + '\n'
    if flags.output is None:
        print(full_exam_str)
    else:
        Path(flags.output).parent.mkdir(parents=True, exist_ok=True)
        with open(flags.output, 'w') as f:
            f.write(full_exam_str)


if __name__ == '__main__':
    flags = parse_args()
    main()
