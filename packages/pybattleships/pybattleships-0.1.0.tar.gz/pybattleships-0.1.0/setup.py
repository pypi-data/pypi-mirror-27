from setuptools import setup

from pybattleships import VERSION

setup(name='pybattleships',
      version=VERSION,
      description='A Python Battleship framework',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
      ],
      keywords='sticky woestgaaf battleship',
      url='http://github.com/RobinSikkens/pybattleships',
      author='Robin Sikkens & Maarten van den Berg',
      author_email='pybattleships@robinsikkens.nl',
      license='MIT',
      packages=['pybattleships'],
      install_requires=[
      ],
      include_package_data=True,
      zip_safe=False
)
