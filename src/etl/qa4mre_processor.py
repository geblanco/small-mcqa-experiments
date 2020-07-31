import json
import argparse

from pathlib import Path
from example import Example

"""
process QA4MRE dataset to RACE-like format, similar to Entrance Exams
"""

flags = None


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input', type=str, required=True, help="Dataset to process"
    )
    parser.add_argument(
        '--output', '-o', type=str, required=False,
        help='Output to write the dataset'
    )
    return parser.parse_args()


def main():
    data = json.load(open(flags.input))
    data = data['test-set']['topic']
    data = [
        datapoint for test in data for datapoint in test['reading-test']
    ]
    examples = [
        Example(
            datapoint['r_id'],
            datapoint['doc']['$t'],
            datapoint['q']
        ).to_json()
        for datapoint in data
    ]
    dataset = dict(version=1.0, data=examples)
    data_str = json.dumps(obj=dataset, ensure_ascii=False) + '\n'
    if flags.output is None:
        print(data_str)
    else:
        Path(flags.output).parent.mkdir(parents=True, exist_ok=True)
        with open(flags.output, 'w') as fout:
            fout.write(data_str)


if __name__ == '__main__':
    flags = parse_args()
    main()
