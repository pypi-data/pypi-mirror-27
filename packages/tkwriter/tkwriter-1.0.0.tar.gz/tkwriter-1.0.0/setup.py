"""A setuptools based setup module""" 
# Always prefer setuptools over distutils    , always give shitty advice no one understands

from setuptools import setup, find_packages

setup(
    name='tkwriter',                                               # Required
    version='1.0.0',                                               # Required 
    description='A GUI text editor using tkinter',                 # Required    
    
    maintainer='dot bit', 
    maintainer_email='dotbit@xx.xx',
    url='https://github.com/pypa/sampleproject',                   #               not Optional
    
    long_description='100 lines of tkinter py3 code to have an editor',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required
)