from setuptools import setup

AUTHOR = 'hirschbeutel'
AUTHOR_EMAIL = 'hirschbeutel@gmail.com'
DESCRIPTION = 'LMD filereader reads LMD files'
LONG_DESCRIPTION = 'read LMD files'
NAME = 'isalmd'
URL='https://bitbucket.org/hirschbeutel/isalmd'

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
