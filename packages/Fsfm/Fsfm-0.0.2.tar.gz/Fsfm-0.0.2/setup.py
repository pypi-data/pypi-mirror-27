from distutils.core import setup
PACKAGE = "Fsfm"  
NAME = "Fsfm"  
DESCRIPTION = "fm rewrite"  
AUTHOR = "Slade Sal"  
AUTHOR_EMAIL = "stw386@sina.com"  
URL = "https://github.com/sladesha/machine_learning/tree/master/FM"  
VERSION = '0.0.2'
  
setup(  
    name=NAME,  
    version=VERSION,  
    description=DESCRIPTION,  
    author=AUTHOR,  
    author_email=AUTHOR_EMAIL,  
    license="Apache License, Version 2.0",  
    url=URL,  
    packages=["Fsfm"],  
    classifiers=[  
        "Development Status :: 3 - Alpha",  
        "Environment :: Web Environment",  
        "Intended Audience :: Developers",  
        "Operating System :: OS Independent",  
        "Programming Language :: Python",  
    ]
) 
