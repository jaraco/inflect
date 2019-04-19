import setuptools


setuptools.setup(
    name="inflect",
    use_scm_version=True,
    description="Correctly generate plurals, singular nouns, ordinals, "
    "indefinite articles; convert numbers to words",
    author="Paul Dyson",
    author_email="pwdyson@yahoo.com",
    maintainer="Alex Gronholm",
    maintainer_email="alex.gronholm@nextday.fi",
    url="https://github.com/jazzband/inflect",
    py_modules=["inflect"],
    provides=["inflect"],
    keywords=["plural", "inflect", "participle"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    install_requires=["importlib_metadata"],
    setup_requires=["setuptools_scm"],
)
