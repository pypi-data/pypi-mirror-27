import argparse


def cli():
    parser = argparse.ArgumentParser(description='Test skeleton creator')
    parser.add_argument('input', type=str, help='filepath of input .py file')
    parser.add_argument(
        '--save', action='store_true', help='save result as test_<input> file')
    return parser.parse_args()
