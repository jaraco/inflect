from distutils.core import setup

setup(name='inflect',
      version='0.1.1',
      description="Correctly generate plurals, ordinals, indefinite articles; convert numbers to words",
      author='Paul Dyson',
      author_email='pwdyson@yahoo.com',
      url="http://pypi.python.org/pypi/inflect",
      py_modules=['inflect'],
      keywords = ['plural', 'inflect', 'participle'],
      classifiers = [
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
        ],
      long_description = open('README.txt').read()
      )
