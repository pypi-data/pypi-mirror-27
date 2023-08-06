from setuptools import setup

setup(
    name='seaborn_parse_doc',
    version='0.0.1',
    description='SeabornParseDoc parses the docstring'
                'of the calling function, then returns'
                'its components in one of several ways.',
    long_description='',
    author='Ben Christenson',
    author_email='Python@BenChristenson.com',
    url='https://github.com/SeabornGames/ParseDoc',
    download_url='https://github.com/SeabornGames/ParseDoc'
                 '/tarball/download',
    keywords=['metadata'],
    install_requires=[],
    extras_require={
    },
    py_modules=['seaborn.parse_doc'],
    license='MIT License',
    packages=['seaborn'],
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: Other/Proprietary License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6'],
    entry_points='''
        [console_scripts]
        parse_doc=seaborn.parse_doc
    ''',
)
