
from setuptools import setup

setup(name='tw_day',
      version='0.1',
      description='Check if the day is holiday/stock market close day',
      url='https://github.com/chunpaiyang/tw_day',
      author='chunpaiyang',
      author_email='chunpaiyang@gmail.com',
      license='MIT',
      packages=['tw_day'],
      package_data={'': ['data/*']},
      zip_safe=False)
