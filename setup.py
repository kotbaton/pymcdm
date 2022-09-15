import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pymcdm",
    version="1.1.0",
    author="Andrii Shekhovtsov, Bartłomiej Kizielewicz",
    author_email="andrii-shekhovtsov@zut.edu.pl, bartlomiej-kizielewicz@zut.edu.pl",
    description="Python library for Multi-Criteria Decision-Making",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/shekhand/mcda",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib'
    ]
)

