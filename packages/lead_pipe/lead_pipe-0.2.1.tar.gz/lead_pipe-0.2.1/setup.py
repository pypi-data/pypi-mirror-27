from distutils.core import setup

with open('README.rst', 'r') as readme:
    long_description = readme.read()

setup(
    name='lead_pipe',
    version='0.2.1',
    description='piping between functions in Python',
    long_description=long_description,
    author='Brett Beatty',
    author_email='brettbeatty@gmail.com',
    url='https://github.com/brettbeatty/lead_pipe',
    packages=['lead_pipe'],
    package_data={'': ['LICENSE', 'README.rst']},
    include_package_data=True,
    keywords=['piping']
)
