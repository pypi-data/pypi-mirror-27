from setuptools import setup, find_packages
import os

print(find_packages())

setup(
    name='vHunter',
    version='0.7',
    author="Patryk Galczynski",
    author_email="galczynski.patryk@gmail.com",
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
    url="http://github.com/evemorgen/vHunter",
    entry_points={
        'console_scripts': ['vhunter = vHunter:main'],
    },
    install_requires=[
        'singleton-decorator',
        'yamlcfg',
        'coloredlogs',
        'aiohttp'
    ],
    packages=find_packages(),
    data_files=[
        ('conf', ['vHunter/conf/' + file for file in os.listdir("vHunter/conf") if file.endswith('.yaml')]),
        ('conf/scenarios', ['vHunter/conf/scenarios/' + file for file in os.listdir("vHunter/conf/scenarios") if file.endswith('.yaml')])
    ],
    include_package_data=True
)
