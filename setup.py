import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='datetime_matcher',
    version='0.1.6',
    author='Stephen Zhao',
    author_email='mail@zhaostephen.com',
    description='A library which extends regex with support for datetime format codes.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=[
        'datetime',
        'regex',
        'datetime parsing',
        'datetime format',
        'find and replace',
        'search and replace',
        'substitution',
        'regular expression',
        'format',
        'strftime',
        'strptime',
        'parse',
        'reformat',
        'date',
        'time',
        'format code',
        'search',
        'find',
        'replace',
        'match',
    ],
    url='https://github.com/stephen-zhao/datetime_matcher',
    packages=setuptools.find_packages('src'),
    package_dir={
        'datetime_matcher': 'src/datetime_matcher'
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
    python_requires='>=3.6',
    license='MIT License'
)