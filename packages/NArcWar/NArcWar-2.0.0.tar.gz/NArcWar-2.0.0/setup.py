from distutils.core import setup

with open('README') as file:
    readme = file.read()

# NOTE: change the 'name' field below with some unique package name.
# then update the url field accordingly.

setup(
    name='NArcWar',
    version='2.0.0',
    packages=['wargame'],
    url='https://upload.pypi.org/legacy/NArcWar/',
    license='LICENSE.txt',
    description='test pkg ignore',
    long_description=readme,
    author='Kamal',
    author_email='infikamal5@gmail.com'
)

