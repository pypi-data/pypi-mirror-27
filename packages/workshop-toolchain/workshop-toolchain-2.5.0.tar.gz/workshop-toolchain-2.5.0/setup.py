from setuptools import setup, find_packages
from gf.version_control import get_version

setup(
    name='workshop-toolchain',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['gf = gf.app_starter:main']
    },
    version=get_version(),
    description='',
    long_description='',
    author='GFA',
    author_email='',
    url='https://github.com/greenfox-academy/huli-workshop-toolchain/',
    install_requires=[
        'PyGithub',
        'python-json-logger',
        'requests',
        'terminaltables'
    ],
)
