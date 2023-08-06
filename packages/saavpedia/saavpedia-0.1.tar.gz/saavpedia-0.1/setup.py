from setuptools import setup, find_packages

setup(name='saavpedia',

      version='0.1',

      url='https://github.com/youngmook/SAAVpedia',

      license='LGPL ver 2.1',

      author='Young-Mook Kang',

      author_email='ymkang@thylove.org',

      description='SAAVpedia 0.1',

      packages=find_packages(exclude=['tests']),

      long_description=open('README.md').read(),

      zip_safe=False,

      setup_requires=['nose>=1.0', 'datetime>=4.0'],

      test_suite='nose.collector')