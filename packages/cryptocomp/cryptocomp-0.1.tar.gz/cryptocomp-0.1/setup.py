from setuptools import setup

setup(name='cryptocomp',
      packages=['cryptocompy'],
      version='0.1',
      description='Simple wrapper for the public Cryptocompare API.',
      keywords = '',
      author='Margarita Rudenskaya',
      author_email='margo.rudenskaya@gmail.com',
      url='https://github.com/wildsmileofbutterfly/cryptocompy',
      download_url='https://github.com/wildsmileofbutterfly/cryptocompy/archive/0.1.1.dev2.tar.gz',
      license='MIT',
      python_requires='>=3',
      install_requires=['requests'],)
