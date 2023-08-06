from setuptools import setup

setup(
     name='encryptFile.py',    # This is the name of your PyPI-package.
     version='0.1',                          # Update the version number for new releases
     scripts=['encryptFile.py -filePath <filePath> -fileName <fileName> -u <cecid>']                  # The name of your scipt, and also the command you'll be using for calling it
 )
