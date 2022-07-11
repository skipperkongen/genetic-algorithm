from setuptools import setup, find_packages

with open("README.md") as fh:
    LONG_DESCRITPION = fh.read()

with open('requirements.txt') as fi:
    REQUIRE = [
        line.strip() for line in fi.readlines()
        if not line.startswith('#')
    ]

with open("version") as fh:
    VERSION = fh.read().strip()

setup(
    name='gaga',
    author="Pimin Konstantin Kefaloukos",
    author_email='skipperkongen@gmail.com',
    url="https://github.com/skipperkongen/gaga",
    version=VERSION,
    description="A genetic algorithm library.",
    long_description=LONG_DESCRITPION,
    long_description_content_type="text/markdown",
    license='unlicence',
    install_requires=REQUIRE,
    data_files=[('',['version', 'requirements.txt'])],
    extras_require={'test': ['pytest', 'flake8', 'pytest-mock']},
    packages=find_packages('src'),
    package_dir={'': 'src'}
)
