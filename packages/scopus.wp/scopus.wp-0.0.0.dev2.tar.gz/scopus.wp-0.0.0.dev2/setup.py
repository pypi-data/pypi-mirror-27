from setuptools import setup

setup(
    name='scopus.wp',
    version='0.0.0.dev2',
    description='A tool for a wordpress server which will automatically post science publications from scopus database',
    url='https://github.com/the16thpythonist/ScopusWp',
    author='Jonas Teufel',
    author_email='jonseb1998@gmail.com',
    license='MIT',
    packages=['scopus'],
    install_requires=[],
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
