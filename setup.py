import re
from setuptools import setup
 
version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('run_command/__init__.py').read(),
    re.M
    ).group(1)
 
setup(
    name = "run_command",
    packages = ["run_command"],
    entry_points = {
        "console_scripts": ['run_command = run_command.main:main']
        },
    version = version,
    description = "Run commands against a host list of machines using SSH keys",
    author = "Kyle Flavin",
    author_email = "",
    url = "https://github.com/kflavin/vim",
    long_description = "Run commands against a host list of machines using SSH keys",
    license = "GPL",
    requires = ['argparse', 'setuptools'],
    install_requires = [
	'argparse',
	'setuptools',
    ],
)
