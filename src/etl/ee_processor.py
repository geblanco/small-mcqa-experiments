import json
import argparse

from example import Example

"""
process Entrance Exams dataset to RACE-like format
sample:
{
    "test-set": {
        "topic": {
            "t_id": "0",
            "t_name": "Entrance Exam",
            "reading-test": [
                {
                    "r_id": "13",
                    "doc": {
                        "d_id": "1",
                        "$t": "<Document.>"
                    },
                    "question": [
                        {
                            "q_id": "1",
                            "q_str": "Question",
                            "answer": [
                                {
                                    "a_id": "1",
                                    "$t": "<ans 1>"
                                },
                                {
                                    "a_id": "2",
                                    "correct": "Yes",
                                    "$t": "<ans 2>"
                                },
                                {
                                    "a_id": "3",
                                    "$t": "<ans 3>"
                                },
                                {
                                    "a_id": "4",
                                    "$t": "<ans 4>"
                                }
                            ]
                        },
                        {...}
"""
# ->
"""
{
    "version": 1.0,
    "language": "spanish",
    "data": [{
        "answers": ["B", ...],
        "options": [
          ["<ans 1>", "<ans 2>", "<ans 3>", "<ans 4>"],
          ...
        ],
        "questions": [
          ["q1", ...]
        ],
        "article": "<Document>",
        "id": ""
    }]
}
"""

flags = None


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input', type=str, required=True, help="Dataset to process"
    )
    return parser.parse_args()


def main():
    data = json.load(open(flags.input))
    data = data['test-set']['topic']['reading-test']
    examples = [
        Example(
            datapoint['r_id'],
            datapoint['doc']['$t'],
            datapoint['question']
        ).to_json()
        for datapoint in data
    ]
    dataset = dict(version=1.0, data=examples)
    print(json.dumps(obj=dataset, ensure_ascii=False))


if __name__ == '__main__':
    flags = parse_args()
    main()
