from subprocess import run
import os
import shlex
import bisect_scanner
from pathlib import Path


try:
    basepath = Path(os.path.dirname(__file__))
    os.chdir(basepath)
except NameError:
    basepath = Path(os.getcwd())


def build():
    for f in basepath.glob('dist/*'):
        os.remove(f)
    run(shlex.split("python setup.py sdist bdist_wheel"), check=True)
    run(shlex.split("twine check dist/*"), check=True)


def publish():
    res = run("twine upload --repository-url https://upload.pypi.org/legacy/ dist/*", shell=True)


def tag():
    version = bisect_scanner.__version__
    tag_name = f'v{version}'
    if len([*basepath.glob(f'dist/bisect_scanner-{version}*')]):
        print(f'Build {version} exists, will be rebuilt')

    if tag_name in run(["git", "tag"], capture_output=True, encoding='utf-8').stdout:
        print(f'Tag {tag_name} exists')
    else:
        run(shlex.split(f'git tag {tag_name}'), check=True)


if __name__ == '__main__':
    tag()
    build()
    publish()
