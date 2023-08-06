from setuptools import setup, find_packages

setup(
    name = 'exp-kit',
    packages = find_packages(exclude=('config')),
    version = '0.0.3',
    description = 'A bunch of scripts facilitating experimentation on AWS.',
    author = 'All-less',
    author_email = 'all.less.mail@gmail.com',
    url = 'https://github.com/All-less/aws-experiment-kit',
    install_requires = [
        'click',
        'boto3',
        'halo',
        'pymongo',
        'paramiko',
        'tabulate'
    ],
    entry_points = {
        'console_scripts': [
            'exp-kit=expkit.cli:main'
        ]
    },
    keywords = [ 'aws' ],
    classifiers = [
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ]
)
