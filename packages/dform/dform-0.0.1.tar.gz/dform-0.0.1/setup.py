from distutils.core import setup

setup(
    name='dform',
    version='0.0.1',
    description='SQL ORM API for pandas DataFrame',
    author = 'HS Moon',
    author_email = 'mhs9089@gmail.com',
    py_modules = ['dform', 'orms'],
    install_requires=['pandas'],
    url='https://github.com/zwolf21/dform'
)