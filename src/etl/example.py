import random


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

    def drop_options(self, keep=None):
        if keep is None or keep > len(self.options[0]):
            raise ValueError(
                'Asked to keep more options than available! '
                f'(asked {keep}/{len(self.options[0])})'
            )
        for i in range(len(self.options)):
            if keep == len(self.options):
                continue
            ans, options = self.answers[i], self.options[i]
            while len(options) > keep:
                correct_index = ord(ans) - ord('A')
                chosen = correct_index
                while chosen == correct_index:
                    chosen = random.choice(range(len(options)))
                del options[chosen]
                if chosen < correct_index:
                    correct_index -= 1
                ans = chr(ord('A') + correct_index)
            self.answers[i], self.options[i] = ans, options

    def to_json(self):
        return self.__dict__
