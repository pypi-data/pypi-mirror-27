from distutils.core import setup
PACKAGE = "fm_easy_run"  
NAME = "fm_easy_run"  
DESCRIPTION = "fm rewrite"  
AUTHOR = "Slade Sal"  
AUTHOR_EMAIL = "sharalion@gmail.com"  
URL = "https://github.com/sladesha/machine_learning/tree/master/FM"  
VERSION = '0.0.1'
  
setup(  
    name=NAME,  
    version=VERSION,  
    description=DESCRIPTION,  
    author=AUTHOR,  
    author_email=AUTHOR_EMAIL,  
    license="Apache License, Version 2.0",  
    url=URL,  
    packages=["fm_easy_run"],  
    classifiers=[  
        "Development Status :: 3 - Alpha",  
        "Environment :: Web Environment",  
        "Intended Audience :: Developers",  
        "Operating System :: OS Independent",  
        "Programming Language :: Python",  
    ]
) 