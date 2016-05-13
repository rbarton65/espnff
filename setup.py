from distutils.core import setup

setup(
    name = 'espnff',
    
    packages = ['espnff'],
    
    version = '0.1.1',
    
    description = 'ESPN fantasy football power rankings algorithm',
    
    author = 'Rich Barton',
    
    author_email = 'rbart65@gmail.com',
    
    packages = ['lxml', 'requests', 'json'],
    
    classifiers = [
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development :: Libraries :: Python Modules',
    ]

)