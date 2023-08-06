from setuptools import setup

with open("Description.txt", 'r') as f:
    long_description = f.read()
setup(
   name='version_hunter',
   version='1.0',
   description='Command line versioning helper for Cx_Freeze / Inno Setup builds.',
   license="MIT",
   long_description=long_description,
   author='Tomasz Kluczkowski',
   author_email='tomaszk1@hotmail.co.uk',
   url="https://github.com/Tomasz-Kluczkowski/versioner",
   packages=['version_hunter'],  #same as name
   install_requires=[], #external packages as dependencies
   scripts=[]
)

