import json
import time
import codecs
import argparse

from googletrans import Translator


FANYI = Translator()


def main():
    parser = create_parser()
    options = vars(parser.parse_args())
    if options['output'] is None:
        options['output'] = 'output-%s.json' % options['dest_language']
    start = time.time()
    translate(options)
    end = time.time()
    time_elapsed = end - start
    print("Translation done in %s seconds" % time_elapsed)


def translate(options):
    with codecs.open(options['locale'], 'r', 'utf-8') as f:
        to_be_translated = json.load(f)

    translated = translate_dict(
        to_be_translated, options['dest_language'])

    with codecs.open(options['output'], 'w', 'utf-8') as o:
        json.dump(translated, o, ensure_ascii=False, indent=4)


def translate_dict(dictionary, dest_language):
    translated = {}

    for key, value in dictionary.items():
        if isinstance(value, dict):
            translated[key] = translate_dict(value, dest_language)
        else:
            google_returns = FANYI.translate(value, dest=dest_language)
            translated[key] = google_returns.text
    return translated


def create_parser():
    parser = argparse.ArgumentParser(
        prog='fy',
        description='')
    parser.add_argument(
        '-d', '--dest-language',
        default='en',
        help='Destination language short code'
    )
    parser.add_argument(
        '-o', '--output',
        help=('select a name for the output file. ' +
              'if omitted, output name is defaulted ' +
              'to output-{dest-language}.json')
    )
    parser.add_argument(
        'locale', metavar='locale.json',
        help=('locale dictionary where keys are engineering tokens ' +
              'and values are actual user interface words')
    )
    return parser


if __name__ == '__main__':
    main()
