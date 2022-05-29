import webbrowser
import subprocess
import argparse


def main(show=False):
    subprocess.run('python -m coverage run -m pytest', shell=True)
    subprocess.run('coverage report -m', shell=True)
    subprocess.run('coverage html', shell=True)
    if show:
        webbrowser.open_new('htmlcov/index.html')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--show', action='store_true', help='open browser with htmlcov/index.html')
    args = parser.parse_args()
    main(show=args.show)
