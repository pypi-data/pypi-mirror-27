from distutils.core import setup

with open('README.rst', 'r') as readme:
    long_description = readme.read()

setup(
    name='hand_grenade',
    version='0.1.1',
    description='the Python dict where close counts',
    long_description=long_description,
    author='Brett Beatty',
    author_email='brettbeatty@gmail.com',
    url='https://github.com/brettbeatty/hand_grenade',
    packages=['hand_grenade'],
    package_data={'': ['LICENSE', 'README.rst']},
    include_package_data=True
)
