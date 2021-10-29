from setuptools import setup
setup(
   name='preprocesspack',
   version='0.0.1',
   author='Nuria Lebena',
   author_email='nlebena001@ehu.eus',
   packages=['preprocesspack', 'preprocesspack.test'],
   url='Indicar una URL para el paquete...',
   license='LICENSE.txt',
   description='Python package with useful functions for data pre-preprocessing',
   long_description=open('README.txt').read(),
   tests_require=['pytest'],
   install_requires=[
      "seaborn >= 0.9.0",
      "pandas >= 0.25.1",
      "matplotlib >= 3.1.1",
      "numpy >=1.17.2"
   ],
)