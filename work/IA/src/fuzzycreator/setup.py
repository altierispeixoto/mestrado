from setuptools import setup

setup(name='fuzzycreator',
      version='1.0',
      description='Create and compare fuzzy sets',
      url='https://bitbucket.org/JosieMcCulloch/fuzzycreator',
      author='Josie McCulloch',
      author_email='josie.mcculloch@nottingham.ac.uk',
      packages=['fuzzycreator', 'fuzzycreator.fuzzy_sets', 'fuzzycreator.membership_functions', 'fuzzycreator.measures'],
      zip_safe=False) 
