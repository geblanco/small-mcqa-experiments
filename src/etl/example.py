answer_indices_to_letters = ['A', 'B', 'C', 'D', 'E']


class Example(object):
    def __init__(self, id, article, questions):
        self.id = id
        self.article = article

        self.questions = self._process_questions(questions)
        self.answers = self._process_answers(questions)
        self.options = self._process_options(questions)

    def _process_questions(self, questions):
        return [q['q_str'] for q in questions]

    def _process_answers(self, questions):
        # get the index of the answer with correct=True
        answers = []
        for question in questions:
            for index, answer in enumerate(question['answer']):
                if answer.get('correct', False):
                    answers.append(answer_indices_to_letters[index])
        return answers

    def _process_options(self, questions):
        options = []
        for question in questions:
            options.append([q['$t'] for q in question['answer']])
        return options

    def to_json(self):
        return self.__dict__
