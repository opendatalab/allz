import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="allz",
    version="0.0.7",
    author="opendatalab",
    author_email="yujia@pjlab.org.cn",
    description="A universal command line tool for compression and decompression",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/opendatalab/allz/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'importlib',
    ],
    python_requires='>=3.7',
    keywords='python, compress, decompress, allz',
    entry_points={'console_scripts': [
        'allz = allz.cli.cmd:cli',
    ]},
)
