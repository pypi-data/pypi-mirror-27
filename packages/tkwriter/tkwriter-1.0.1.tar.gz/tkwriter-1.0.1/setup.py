"""A setuptools based setup module""" 
# Always prefer setuptools over distutils , always give condescending advice no one understands and non-working sample projects

from setuptools import setup, find_packages

setup(
    
    py_modules=["tkwriter"],
    
    name='tkwriter',                                               # Required
    version='1.0.1',                                               # Required 
    description='A GUI text editor using tkinter',                 # Required    
    
    maintainer='dot bit', 
    maintainer_email='dotbit@xx.xx',
    url='https://github.com/pypa/sampleproject',                   #               not Optional
    
    entry_points={                                                 # Optional ??
        'console_scripts': [
            'tkwriter=tkwriter:main',
        ],
    },
                                                                   # Optional
        classifiers=[  
        'Programming Language :: Python :: 3.6',
    ],

    keywords='tkinter editor GUI text',                            # Optional
    
    long_description='100 lines of tkinter py3 code to have an editor',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required
)