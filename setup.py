import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

requires = [
    'boto==2.18.0',
    'python-dateutil==2.2'
]

entry_points = {
    'console_scripts' : [
        'electric_sync = electricity.scripts.electric_sync:main',
    ]
}

setup(name='electricity',
    version='0.1',
    description='Static asset manager',
    url='http://github.com/digitaldreamer/electricity',
    author='digitaldreamer',
    author_email='',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    entry_points=entry_points,
    zip_safe=False,
)
