from distutils.core import setup

with open('README.rst', 'r') as readme:
    long_description = readme.read()

setup(
    name='matchstick',
    version='0.1.1',
    description='Pattern matching in Python',
    long_description=long_description,
    author='Brett Beatty',
    author_email='brettbeatty@gmail.com',
    url='https://github.com/brettbeatty/matchstick',
    packages=['matchstick'],
    package_data={'': ['LICENSE', 'README.rst']},
    include_package_data=True,
    keywords=['pattern', 'match', 'overload']
)
