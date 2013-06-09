from distutils.core import setup
import os

import inflect


here = os.path.dirname(__file__)
readme_path = os.path.join(here, 'README.rst')
readme = open(readme_path).read()

setup(
    name='inflect',
    version=inflect.__version__,
    description='Correctly generate plurals, singular nouns, ordinals, indefinite articles; convert numbers to words',
    long_description=readme,
    author='Paul Dyson',
    author_email='pwdyson@yahoo.com',
    maintainer='Alex Gronholm',
    maintainer_email='alex.gronholm@nextday.fi',
    url='http://pypi.python.org/pypi/inflect',
    py_modules=['inflect'],
    provides=['inflect'],
    keywords=['plural', 'inflect', 'participle'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Linguistic',
    ]
)
