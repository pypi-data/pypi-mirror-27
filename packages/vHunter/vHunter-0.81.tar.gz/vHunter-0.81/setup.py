from setuptools import setup, find_packages
import os

REQUIREMENTS = [
    "singleton-decorator==1.0.0",
    "yamlcfg==0.5.3",
    "coloredlogs==7.3",
    "aiohttp==2.3.6",
    "setproctitle==1.1.10",
    "daemonize==2.4.7"
]
open("vHunter/requirements.txt", "w").writelines(req + "\n" for req in REQUIREMENTS)

setup(
    name='vHunter',
    version='0.81',
    author="Patryk Galczynski",
    author_email="galczynski.patryk@gmail.com",
    license='MIT',
    long_description=open('README.md').read(),
    url="http://github.com/evemorgen/vHunter",
    entry_points={
        'console_scripts': ['vhunter = vHunter:main'],
    },
    install_requires=REQUIREMENTS,
    packages=find_packages(),
    data_files=[
        ('conf', ['vHunter/conf/' + file for file in os.listdir("vHunter/conf") if file.endswith('.yaml')]),
        ('conf/scenarios', ['vHunter/conf/scenarios/' + file for file in os.listdir("vHunter/conf/scenarios") if file.endswith('.yaml')])
    ],
    include_package_data=True
)
