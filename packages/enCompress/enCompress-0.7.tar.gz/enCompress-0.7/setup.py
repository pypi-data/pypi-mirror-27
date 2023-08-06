from setuptools import setup

setup(
     name='enCompress',    # This is the name of your PyPI-package.
     version='0.7',                          # Update the version number for new releases
     description='Creates a password protected compressed file',
     install_requires=['pyminizip'],
     python_requires='>=3',
     entry_points={
          'console_scripts': [
              'encode_compress=encode_compress.enCrypt.encodeFile'
          ]
      },

 )

