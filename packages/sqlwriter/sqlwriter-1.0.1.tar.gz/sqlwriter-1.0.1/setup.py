import subprocess as sp
import sys

from setuptools import setup


def check():
    """Check the source code to make sure there are no syntax failures"""
    cmd = "python -m pyflakes ."
    p = sp.Popen(cmd, shell=True, stdout=sp.PIPE)
    p.wait()
    out, err = p.communicate()
    if out:
        print('PYFLAKES:')
        print(out)
        sys.exit(1)


def do_setup():
    check()
    setup(
        name='sqlwriter',
        description="Writes pandas DataFrame to several flavors of sql database",
        license="MIT",
        version='1.0.1',
        packages=['sqlwriter', ],
        install_requires=[],  # things that need to be installed before package
        classifiers=[
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2.7'
        ]
    )


if __name__ == '__main__':
    do_setup()
