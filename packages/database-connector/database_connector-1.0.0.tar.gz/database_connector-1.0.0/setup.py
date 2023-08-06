from setuptools import setup

setup(name='database_connector',
      version='1.0.0',
      description='Database Connector class',
      url='https://dgdgit.chop.edu/DGD/Database_Connector',
      author='Adam Gleason',
      author_email='gleasona@email.chop.edu',
      license='MIT',
      packages=['database_connector'],
      install_requires=['cx_Oracle', 'pymysql', 'pymongo'],
      zip_safe=False)
