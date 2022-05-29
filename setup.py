from pathlib import Path
from setuptools import setup

# Read requirements
requirements = Path(__file__).parent.joinpath('requirements.txt').read_text('ascii', 'ignore')
requirements = requirements.replace(u'\x00', '').replace('\r', '').split('\n')

# Read description
long_description = Path(__file__).parent.joinpath('README.md').read_text()

setup(
    name='docrecer',
    version='0.0.1',
    description='Document recognizer (passport, patent, snils and migration card)',
    long_description=long_description,
    author='Karimzhonov Khusniddin',
    author_email='khtkarimzhonov@mail.ru',
    url='https://github.com/karimzhonov/docrecer',
    install_requires=requirements,
)
