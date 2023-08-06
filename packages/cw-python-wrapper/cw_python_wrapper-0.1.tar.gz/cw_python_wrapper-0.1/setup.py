from setuptools import setup

setup(name='cw_python_wrapper',
      version='0.1',
      description='Python wrapper for Code Wars',
      author='Michiel Dockx',
      author_email='michieldx@gmail.com',
      url='https://bitbucket.org/Arvraepe-jstack/codewars',
      packages=['cw-python-wrapper'],
      install_requires=[
          'socketIO_client_nexus==0.7.6',
      ])
