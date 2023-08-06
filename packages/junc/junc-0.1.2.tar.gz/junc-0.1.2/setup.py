from setuptools import setup, find_packages
from codecs import open
from os import path

from junc import VERSION

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='junc',
    version=VERSION,
    description='Connect to servers easily',
    long_description=long_description,
    url='https://github.com/llamicron/junc',
    author='Luke Sweeney',
    author_email='llamicron@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.4',
        # 'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='connect ip ssh pipe raspberry pi rpi raspberry-pi ec2 server',
    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    py_modules=["junc", "storage", "server"],
    #
    # packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['docopt'],
    extras_require={
        'dev': ['twine'],
        'test': ['coverage', 'pytest']
    },
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    entry_points={  # Optional
        'console_scripts': [
            'junc=junc:main',
        ],
    },
)
