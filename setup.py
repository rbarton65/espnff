from setuptools import setup

setup(
    name='espnff',

    packages=['espnff'],

    include_package_data=True,

    version='1.0.0',

    description='ESPN fantasy football API',

    author='Rich Barton',

    author_email='rbart65@gmail.com',

    install_requires=['requests', 'numpy'],

    url='https://github.com/rbarton65/espnff',

    classifiers=[
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
