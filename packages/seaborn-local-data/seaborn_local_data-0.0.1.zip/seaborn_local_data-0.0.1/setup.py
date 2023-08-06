from setuptools import setup

setup(
    name='seaborn_local_data',
    version='0.0.1',
    description='SeabornLocalData allows for the easy'
				'storage and parsing of data stored in'
				'local files',
    long_description='',
    author='Ben Christenson',
    author_email='Python@BenChristenson.com',
    url='https://github.com/SeabornGames/LocalData',
    download_url='https://github.com/SeabornGames/LocalData'
                 '/tarball/download',
    keywords=['data'],
    install_requires=[],
    extras_require={
    },
    py_modules=['seaborn.file'],
    license='MIT License',
    packages=['seaborn'],
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: Other/Proprietary License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6'],
    entry_points='''
        [console_scripts]
        local_data=seaborn.local_data
    ''',
)
