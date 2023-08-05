from setuptools import setup
from os import path
# Get a handle on where we're at :)
here = path.abspath(path.dirname(__file__))

setup(
    name='pytimgr',
    version='0.0.1',
    author='Alex Caudill',
    author_email='alex.caudill@protonmail.com',
    url='https://github.com/televidence/pytimgr',
    description='Python tidy container lifecycle management',
    packages=['pytimgr', 'pytimgr.tipd', 'pytimgr.tikv', 'pytimgr.tidb'],
    platforms="Linux, Mac OS X",
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    entry_points = {
     'console_scripts': [
      'pytimgr = pytimgr.cmd:main',
     ],
    }
)
