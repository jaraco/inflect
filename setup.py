from distutils.core import setup
setup(name='inflect',
      version='0.1',
      description="Correctly generate plurals, ordinals, indefinite articles; convert numbers to words",
      author='Paul Dyson',
      author_email='pwdyson@yahoo.com',
      py_modules=['inflect'],
      keywords = ['plural', 'inflect', 'participle'],
      classifiers = [
        "Programming Language :: Python",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
        ],
      long_description = """\
Generate Inflections
--------------------

* generate plural nouns
* generate plural verbs
* test if a word is the plural of another
* generate 'a' or 'an' correctly before a noun
* generate ordinal numbers
* convert numbers into text
""",
      )
