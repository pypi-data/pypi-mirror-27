from setuptools import setup, find_packages

setup(
  name = 'choptools',
  packages = ['choptools'], # this must be the same as the name above
  version = '0.1',
  description = 'Python script to chop proteins and prepare z-matrices needed for MCPRO simulations.',
  author = 'Matthew C. Robinson, Israel Cabeza de Vaca Lopez',
  author_email = 'matthew.robinson@yale.edu',
  license='MIT',
  url='https://github.com/mc-robinson/choptools',
  keywords = ['computational chemistry', 'force fields', 'molecular dynamics'],
  classifiers = [
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering',
        ],
  install_requires=['biopandas'],
  entry_points={
        'console_scripts': [
            'pdb2zmat=choptools.pdb2zmat:main',
        ],
    },

)
