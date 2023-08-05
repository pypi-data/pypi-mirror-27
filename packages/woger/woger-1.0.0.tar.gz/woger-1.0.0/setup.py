from setuptools import find_packages, setup


NAME = 'woger'
DESCRIPTION = 'Workspace manager library'
URL = 'https://gitlab.com/grhiabor/woger'
EMAIL = 'grihabor@mail.ru'
AUTHOR = 'Borodin Gregory'

REQUIRED = [

]

setup(
    name=NAME,
    version='1.0.0',
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    install_requires=REQUIRED,
    include_package_data=True,
    license='MIT',
)
