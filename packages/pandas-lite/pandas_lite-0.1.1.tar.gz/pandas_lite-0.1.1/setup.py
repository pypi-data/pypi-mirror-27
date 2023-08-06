from setuptools import setup, find_packages

setup(name='pandas_lite',
      version='0.1.1',
      description='A lighter version of pandas. No Series, No hierarchical '
                  'indexing, only one indexer [ ]',
      url='https://github.com/tdpetrou/pandas_lite',
      author='Ted Petrou',
      author_email='petrou.theodore@gmail.com',
      license='BSD 3-clause',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.6'],
      keywords='data pandas aggregation',
      packages=find_packages(exclude=['docs', 'stubs']),
      install_requires=['numpy'],
      python_requires='>=3.6')
