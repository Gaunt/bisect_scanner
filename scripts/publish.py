from subprocess import run
import os
import shlex
from pathlib import Path
from sys import version


try:
    basepath = (
        (Path(os.path.dirname(__file__)) / Path("..")).absolute().resolve()
    )
except NameError:
    basepath = (Path(os.getcwd()) / Path("..")).absolute().resolve()


with open(basepath / "version.py") as f:
    __version__ = ''
    exec(f.read())
    assert __version__
    version = __version__


def build():
    for f in basepath.glob("dist/*"):
        print(f'removing {f}')
        os.remove(f)
    setup_path = basepath / "setup.py"
    run(shlex.split(f"python {setup_path} sdist bdist_wheel"), check=True)
    run(shlex.split(f"twine check {basepath / 'dist'}/*"), check=True)


def publish():
    res = run(
        f"twine upload --repository-url https://upload.pypi.org/legacy/ {basepath / 'dist'}/* --verbose",
        shell=True,
    )


def tag():
    tag_name = f"v{version}"
    if len([*basepath.glob(f"dist/bisect_scanner-{version}*")]):
        print(f"Build {version} exists, will be rebuilt")

    if (
        tag_name
        in run(["git", "tag"], capture_output=True, encoding="utf-8").stdout
    ):
        print(f"Tag {tag_name} exists")
    else:
        run(shlex.split(f"git tag {tag_name}"), check=True)


if __name__ == "__main__":
    tag()
    build()
    publish()
