import os, sys, re

# get version info from module without importing it
version_re = re.compile("""__version__[\s]*=[\s]*['|"](.*)['|"]""")

with open('screwdriver.py') as f:
    content = f.read()
    match = version_re.search(content)
    version = match.group(1)


readme = os.path.join(os.path.dirname(__file__), 'README.rst')
long_description = open(readme).read()


SETUP_ARGS = dict(
    name='screwdriver',
    version=version,
    description=('Collection of random python tools and utilities '),
    long_description=long_description,
    url='https://github.com/cltrudeau/screwdriver',
    author='Christopher Trudeau',
    author_email='ctrudeau+pypi@arsensa.com',
    license='MIT',
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='tools',
    test_suite='load_tests.get_suite',
    py_modules = ['screwdriver',],
    install_requires = [
        'six>=1.10',
    ],
    tests_require=[
        'waelstow>=0.10.1',
    ],
)

if __name__ == '__main__':
    from setuptools import setup, find_packages

    SETUP_ARGS['packages'] = find_packages()
    setup(**SETUP_ARGS)
