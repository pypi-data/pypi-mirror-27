
import os
import sys

from setuptools import setup, find_packages

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    os.system("python setup.py bdist_wheel upload")
    sys.exit()

setup(
    name="hanlp-wrapper",
    description="HanLP wrapper in python",
    url="https://github.com/longquanj/HanLP-py.git",
    author="Longquan JIANG",
    author_email="longquan.jiang@outlook.com",
    version="0.1.2",
    license="Apache License 2.0",
    keywords="hanlp python segment",
    install_requires=[
        "pyyaml",
        "JPype1"
    ],
    platforms=[
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows :: Windows 7',
        'Operating System :: Microsoft :: Windows :: Windows Vista',
        'Operating System :: POSIX :: Linux',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities'
    ],
    packages=find_packages(),
    package_dir={'hanlp': 'hanlp'},
    zip_safe=False
)