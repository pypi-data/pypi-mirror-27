from setuptools import setup

setup(
    name='scopus.wp',
    version='0.0.0.dev7',
    description='A tool for a wordpress server which will automatically post science publications from scopus database',
    url='https://github.com/the16thpythonist/ScopusWp',
    author='Jonas Teufel',
    author_email='jonseb1998@gmail.com',
    license='MIT',
    packages=['scopus'],
    install_requires=[
        'requests>=2.0',
        'mysqlclient>=1.2',
        'unidecode>=0.4',
        'tabulate>=0.8',
        'python-wordpress-xmlrpc>=2.3'
    ],
    python_requires='>=3, <4',
    package_data={
        '': ['*.sql']
    },
    py_modules=[
        'install',
        'main',
        'data',
        'database',
        'controller',
        'config',
        'test',
        'view',
        'wordpress',
        'reference'
    ]
)
