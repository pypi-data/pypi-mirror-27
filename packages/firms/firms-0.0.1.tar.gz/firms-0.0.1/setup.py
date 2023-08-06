from setuptools import setup

setup(
    name='firms',
    version='0.0.1',
    description='Fuzzy Information Retrieval for Musical Scores',
    url='https://github.com/axiomabsolute/cs410-information-retrieval',
    download_url='https://github.com/axiomabsolute/cs410-information-retrieval/archive/0.0.1.tar.gz',
    author='Devon Terrell',
    author_email='devon@axioms.me',
    license='MIT',
    packages=['firms'],
    python_requires=">=3",
    install_requirements=[
        'music21',
        'tabulate',
        'click',
        'scipy'
    ])