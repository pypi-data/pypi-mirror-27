from setuptools import setup

AUTHOR = 'hirschbeutel'
AUTHOR_EMAIL = 'hirschbeutel@gmail.com'
DESCRIPTION = 'LMI GFM FD3 filereader'
LONG_DESCRIPTION = 'read FD3 files'
NAME = 'mikrocad'
URL='https://bitbucket.org/hirschbeutel/mikrocad'

with open('VERSION') as version_file:
    VERSION = version_file.read().strip()

setup(
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        description=DESCRIPTION,
        license='LGPL',
        long_description=LONG_DESCRIPTION,
        name=NAME,
        packages=[NAME],
        version=VERSION,
        url=URL,)
