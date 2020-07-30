import setuptools

setuptools.setup(
    name="p4e",
    version="0.0.1",
    author="Mike Matera",
    author_email="matera@lifealgorithmic.com",
    description="Python for Everyone Courseware",
    url="http://www.lifealgorithmic.com",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],

    install_requires=[
        'pexpect', 
        'requests_unixsocket',
        'flask',
    ],

    packages=[
        'p4e', 
    ],
    
    scripts=[
    ],

)