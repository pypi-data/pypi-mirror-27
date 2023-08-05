from setuptools import setup
from vtrtool import __version__

setup(
    name='vtrtool',
    version=__version__,
    author='Tim Lin (S-Cube)',
    author_email='tlin@s-cube.com',
    description='Python utilities for Fullwave3D VTR model files',
    license='3-clause BSD',
    keywords='fullwave3d vtr',
    url='http://not-yet',
    py_modules=['vtrtool'],
    long_description=open('README.md').read(),
    install_requires=[
        'numpy',
        'docopt'
    ],
    scripts=['vtrtool'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
    ]
)
