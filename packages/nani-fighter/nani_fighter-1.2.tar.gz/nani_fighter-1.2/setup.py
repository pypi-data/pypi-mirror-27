from setuptools import setup

setup(
    name='nani_fighter',
    packages=['nani_fighter'],
    include_package_data=True,
    version='1.2',
    description='A Simple Game',
    long_description=open("README.md").read(),
    author='Fazle Rahat',
    author_email='fr.rahat@gmail.com',
    license='MIT',
    url='https://github.com/frrahat/Nani-Fighter',  
    download_url='https://github.com/frrahat/Nani-Fighter/archive/1.2.tar.gz', 
    keywords=['game', 'school', 'shooting'],
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        'pygame',
    ],
)
