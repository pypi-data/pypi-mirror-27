from setuptools import setup, find_packages

setup(
     name='enCompress',    # This is the name of your PyPI-package.
     version='1.4',                          # Update the version number for new releases
     packages=find_packages(),
     description='Creates a password protected compressed file',
     install_requires=['pyminizip'],
     python_requires='>=3',
     entry_points={
          'console_scripts': [
              'en_compress=encode_compress.enCrypt.main'
          ]
      },

 )

