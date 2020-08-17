import os
import json
import argparse

from pathlib import Path
from mcqa_utils.dataset import Dataset

"""
process QA4MRE in RACE-like format to train/dev/test splits by language
"""

flags = None
languages = ['ar', 'bg', 'de', 'en', 'es', 'it', 'ro']


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input', type=str, required=True,
        help="Data dir with year-language files"
    )
    parser.add_argument(
        '-o', '--output', type=str, required=False,
        help='Output to write the dataset'
    )
    parser.add_argument(
        '-p', '--proportions', nargs='*', required=False,
        help='Proportions to split the dataset in train/dev/test'
    )
    parser.add_argument(
        '-s', '--save_full', required=False, action='store_true',
        help='Whether to save the full dataset as a single split'
    )
    parser.add_argument(
        '-S', '--seed', default=42, help='Seed to randomize splits'
    )
    return parser.parse_args()


def write_lang_split(json_examples, output_path):
    data_str = json.dumps(json_examples, ensure_ascii=False) + '\n'
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as fout:
        fout.write(data_str)


def process_lang_dataset(dataset, lang_glob, lang_output_dir):
    examples = dataset.get_all_examples(lang_glob)
    if flags.save_full:
        all_fname = 'all.json'
        all_output_path = os.path.join(lang_output_dir, all_fname)
        write_lang_split(dataset.to_json(examples), all_output_path)
    return examples


def process_splits(dataset, lang_examples, lang_output_dir):
    train, dev, test = dataset.split_examples(
        examples=lang_examples,
        proportions=flags.proportions,
        seed=flags.seed,
    )
    zipped = zip(['train', 'dev', 'test'], [train, dev, test])
    for set_name, set_data in zipped:
        set_fname = f'{set_name}.json'
        set_output_path = os.path.join(lang_output_dir, set_fname)
        write_lang_split(dataset.to_json(set_data), set_output_path)


def main():
    if flags.output is None:
        flags.output = flags.input

    if flags.proportions is None:
        flags.proportions = [0.6, 0.2, 0.2]

    dataset = Dataset(data_path=flags.input, task='generic')
    lang_file_globs = [f'{flags.input}/*{lang}*.json' for lang in languages]
    
    for lang, lang_glob in zip(languages, lang_file_globs):
        lang_dir = os.path.join(flags.output, lang)
        lang_examples = process_lang_dataset(dataset, lang_glob, lang_dir)
        process_splits(dataset, lang_examples, lang_dir)


if __name__ == '__main__':
    flags = parse_args()
    main()
