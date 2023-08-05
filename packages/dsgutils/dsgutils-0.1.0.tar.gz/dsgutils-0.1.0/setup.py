from setuptools import setup, find_packages

setup(name='dsgutils',
      version='0.1.0',
      description='Utility functions for common data science operations and visualizations',
      url='https://github.com/datascienceisrael/python3-dsgutils',
      download_url='https://github.com/datascienceisrael/python3-dsgutils/archive/0.1.1.tar.gz',
      author='Data Science Group',
      author_mail='elior@datascience.co.il',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'pandas',
      ])