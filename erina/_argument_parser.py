import argparse

args = None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Some config stuff')

    parser.add_argument(
        '--no-stdout',
        action='store_true',
        help='debug to console (default True)'
    )

    args = parser.parse_args()
