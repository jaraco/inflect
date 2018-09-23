import os
import io

import inflect

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


here = os.path.dirname(__file__)
readme_path = os.path.join(here, 'README.rst')
readme = io.open(readme_path, encoding='utf-8').read()

setup(
    name='inflect',
    version=inflect.__version__,
    description='Correctly generate plurals, singular nouns, ordinals, '
                'indefinite articles; convert numbers to words',
    long_description=readme,
    author='Paul Dyson',
    author_email='pwdyson@yahoo.com',
    maintainer='Alex Gronholm',
    maintainer_email='alex.gronholm@nextday.fi',
    url='https://github.com/jazzband/inflect',
    py_modules=['inflect'],
    provides=['inflect'],
    keywords=['plural', 'inflect', 'participle'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Linguistic',
    ],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    setup_requires=[
        'setuptools_scm',
    ],
)
