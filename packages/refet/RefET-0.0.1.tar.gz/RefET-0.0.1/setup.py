try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

tag = '0.0.1'

setup(name='RefET',
      version=tag,
      description='Standardized Reference ET functions',
      license='Apache',
      author='Charles Morton',
      author_email='charles.g.morton@gmail.com',
      url='https://github.com/cgmorton/RefET',
      install_requires=['numpy'],
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      packages=['refet'],
      keywords='RefET Evapotranspiration',
      classifiers = [
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
      ],
)
