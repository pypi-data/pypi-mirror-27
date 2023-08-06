from setuptools import setup

version = '1.0.2'

setup(name='simMachines',
      scripts = ['simMachines.py'],
      install_requires=['requests','base64','json','numpy','getpass','os','pandas'],
      version=version,
      description="A library to use simMachines, Inc. API",
      python_requires='>=3',
      author = 'Rick Palmer',
      author_email = 'rickpalmer@simmachines.com'
      )