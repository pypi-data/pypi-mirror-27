try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

tag = '0.0.2'

setup(name='RefET',
      version=tag,
      description='ASCE Standardized Reference Evapotranspiration Functions',
      license='Apache',
      author='Charles Morton',
      author_email='charles.g.morton@gmail.com',
      url='https://github.com/cgmorton/RefET',
      download_url = 'https://github.com/{}/{}/archive/v{}.tar.gz'.format('cgmorton', 'RefET', tag),
      install_requires=['numpy'],
      setup_requires=['pytest-runner'],
      tests_require=['pytest', 'pandas', 'pytz'],
      packages=['refet'],
      keywords='RefET Evapotranspiration',
      classifiers = [
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
      ],
)
