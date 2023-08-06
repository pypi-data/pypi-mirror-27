"""Setup script for write-me Python package."""
from setuptools import setup


setup(
    name='write_me',
    packages=['readme_generator'],
    entry_points={
        'console_scripts': ['genreadme = readme_generator.make_scaffold:main'],
    },
    version='0.2',
    description='Python package to assist developers with constructing README as project evolves.',
    author=['Chelsea Dole',
            'Matt Favoino',
            'Darren Haynes',
            'Chris Closser',
            'Gabriel Meringolo'],
    author_email='chelseadole@gmail.com',
    url='https://github.com/chelseadole/write-me',
    download_url='https://github.com/chelseadole/write-me/archive/0.2.tar.gz',
    keywords=['Python', 'README', 'PyPi', 'pip'],
    classifiers=[],
    install_requires=[
        "markdown-generator==0.1.3",
    ],
)
