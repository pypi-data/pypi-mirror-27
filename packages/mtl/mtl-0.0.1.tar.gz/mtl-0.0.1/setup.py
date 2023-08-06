from setuptools import setup

setup(
    name='mtl',
    version='0.0.1',
    description='moving time lapse',
    long_description=open('README.rst').read(),
    keywords='time-lapse barnacle',
    url='https://github.com/jinyung/mtl',
    author='Wong Jin Yung',
    author_email='wongjinyung@gmail.com',
    packages=['mtl'],
    entry_points={
        'console_scripts': ['mtl=mtl.mtl:main'],
    },
    license='MIT',
    install_requires=[
        'numpy',
	'argparse'
    ]
)
