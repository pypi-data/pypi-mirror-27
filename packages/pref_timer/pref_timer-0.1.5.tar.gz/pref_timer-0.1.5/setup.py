import os
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
      name='pref_timer',
      version='0.1.5',
      description='Used to find the function execution time',
      url='https://github.com/PraveenJP/pyPerformanceTimer',
      author='Praveen J',
      author_email='praveen.josephmasilamani@outlook.com',
      license='MIT',
      long_description=read('README.rst'),
      packages=['pref_timer'],
      keywords=['performance', 'testing', 'execution'],
      classifiers = [],
)