import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='datetime_matcher',
    version='0.1.2',
    author='Stephen Zhao',
    author_email='mail@zhaostephen.com',
    description='A library which extends regex with support for datetime format codes.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/stephen-zhao/datetime_matcher',
    packages=setuptools.find_packages('src'),
    package_dir={
        'datetime_matcher': 'src/datetime_matcher'
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)