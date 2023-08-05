import os
from setuptools import find_packages, setup


NAME = 'woger'
DESCRIPTION = 'Workspace manager library'
URL = 'https://gitlab.com/grhiabor/woger'
EMAIL = 'grihabor@mail.ru'
AUTHOR = 'Borodin Gregory'

REQUIRED = ['setuptools']


def get_version():
    project_path = os.path.abspath(os.path.join(__file__, os.pardir))
    init_path = os.path.join(project_path, 'woger', '__init__.py')
    with open(init_path, 'r') as f:
        for line in f:
            if line.startswith('__version__'):
                version_string = line.split('=')[-1].strip()
                return version_string.strip("'")


def main():
    setup(
        name=NAME,
        version=get_version(),
        description=DESCRIPTION,
        author=AUTHOR,
        author_email=EMAIL,
        url=URL,
        packages=find_packages(exclude=('tests',)),
        install_requires=REQUIRED,
        include_package_data=True,
        license='MIT',
    )


if __name__ == '__main__':
    main()
