#!/usr/bin/python3.5

from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='binary_clock',
      version='0.0.2',
      description='Truly Binary Clock',
      long_description=readme(),
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities',
      ],
      keywords='binary clock',
      url='https://github.com/zeycus/binary_clock/',
      author='Miguel Garcia (aka Zeycus)',
      author_email='zeycus@gmail.com',
      license='MIT',
      platforms=['Windows', 'Linux'],
      packages=['binary_clock'],
      install_requires=[],
      include_package_data=True,
      scripts=['bin/binclock.py'],
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'],
)