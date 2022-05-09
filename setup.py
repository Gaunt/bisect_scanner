from pathlib import Path
from setuptools import find_packages
from setuptools import setup
from pathlib import Path
import os
#from bisect_scanner.version import __version__


__version__ = "0.1.10"


try:
    from pip._internal.req import parse_requirements
except ImportError:
    from pip.req import parse_requirements


basepath = Path(os.path.dirname(__file__))
    
requirements_path = basepath / Path("requirements.txt")
install_reqs = [*parse_requirements(str(requirements_path), session="hack")]

try:
    reqs = [str(ir.req) for ir in install_reqs]
except AttributeError:
    reqs = [str(ir.requirement) for ir in install_reqs]

README = (Path(__file__).absolute().parent / "README.md").read_text()


setup(
    name="bisect_scanner",
    version=__version__,
    url="https://github.com/Gaunt/bisect_scanner",
    license="MIT",
    author="Karel Novak",
    author_email="novakk5@gmail.com",
    description="Scan for balance history",
    long_description_content_type="text/markdown",
    long_description=README,
    packages=find_packages(exclude=("tests",)),
    install_requires=reqs,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
