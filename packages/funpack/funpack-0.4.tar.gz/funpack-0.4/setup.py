from setuptools import setup

setup(name='funpack',
      version='0.4',
      description='Get google home link repond',
      url='https://github.cerner.com/cs049571/lib_dep_tryouts',
      author='Chintan Soni',
      author_email='chintan.soni@cerner.com',
      license='Cerner',
      packages=['funpack'],
      install_requires=[
          'requests'
      ],
      zip_safe=False)
