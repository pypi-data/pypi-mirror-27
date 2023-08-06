from setuptools import setup

version = '1.0.9'

setup(name='simMachines',
      packages = ['simMachines'],
      install_requires=['requests','numpy','pandas'],
      version=version,
      description="A library to use simMachines, Inc. API",
      python_requires='>=3',
      author = 'Rick Palmer',
      author_email = 'rickpalmer@simmachines.com'
      )
