from setuptools import setup

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()
with open("version.txt") as f:
    version = f.read()

setup(
    name='Tokage',
    author='SynderBlack',
    version=version,
    packages=['tokage'],
    license='MIT',
    description='Async wrapper for the MyAnimeList API',
    include_package_data=True,
    install_requires=requirements
)
