from distutils.core import setup

import inflect


setup(name='inflect',
      version=inflect.__version__,
      description="Correctly generate plurals, singular nouns, ordinals, indefinite articles; convert numbers to words",
      author='Paul Dyson',
      author_email='pwdyson@yahoo.com',
      url="http://pypi.python.org/pypi/inflect",
      py_modules=['inflect'],
      provides=['inflect'],
      keywords = ['plural', 'inflect', 'participle'],
      classifiers = [
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
        ],
      long_description = open('README.txt').read()
      )
